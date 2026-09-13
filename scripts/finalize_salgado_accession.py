"""Build a dated Salgado admission amendment for independent review.

Reads the immutable, independently reviewed intake commit. It never supplies a
reviewer or a GitHub approval. Review sealing is a separate, receipt-bound act.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess

import migrate_public_entities as m

ROOT = Path(__file__).resolve().parents[1]
INTAKE = '4939941ae69d5edf0eec86712186add1666ab410'
LOT = '6529NM.2026.004'
BASE = f'records/accessions/{LOT}'
CERT = '6529NM-ACC-2026-004'
GAA = LOT + '.GAA-01'
WAVE = '6529NM-WAVE-OBS-2026-09-13-003'
ACTOR = 'codex-task:01a087a1-5e64-7280-b5f8-82d0df4ec066'
EVIDENCE = 'evidence/salgado-amazonia-admission'
REVIEWER = 'codex-reviewer:salgado-2026-09-13-independent'
REVIEW_ID = '6529NM.2026.004.REVIEW-AI-20260913-01'
SOURCE_RECEIPT = 'notes/wip/2026-09-13-salgado-review-receipt.json'
SOURCE_REVIEW = 'notes/wip/2026-09-13-salgado-independent-review.md'


def verify_intake_approval(receipt, read_blob= None):
    """Require the exact appointed approval and every original reviewed byte."""
    read_blob = read_blob or old_bytes
    expected = {'receipt_type': 'MUSEUM_INDEPENDENT_REVIEW_COMMIT_BINDING',
                'review_id': REVIEW_ID, 'reviewer_id': REVIEWER,
                'review_outcome': 'approved', 'reviewed_commit_sha': INTAKE}
    if any(receipt.get(key) != value for key, value in expected.items()):
        raise ValueError('The intake requires its exact independent approved commit-binding receipt.')
    for key, path in [('source_receipt', SOURCE_RECEIPT), ('source_review_artifact', SOURCE_REVIEW)]:
        reference = receipt.get(key, {})
        if (reference.get('path') != path or reference.get('source_commit_sha') != INTAKE
                or sha(read_blob(path)) != 'sha256:' + reference.get('raw_sha256', '')):
            raise ValueError(f'Independent review source identity or fixity mismatch: {key}')
    source = json.loads(read_blob(SOURCE_RECEIPT))
    if (source.get('review_id') != REVIEW_ID or source.get('reviewer_id') != REVIEWER
            or source.get('review_outcome') != 'approved'
            or receipt.get('files') != source.get('files')):
        raise ValueError('Independent review source approval or file inventory mismatch.')
    files = source.get('files', [])
    if len(files) != 70 or len({item['path'] for item in files}) != 70:
        raise ValueError('Independent review requires the complete unique 70-file intake inventory.')
    for item in files:
        if sha(read_blob(item['path'])) != 'sha256:' + item['raw_sha256']:
            raise ValueError(f"Independent review file fixity mismatch: {item['path']}")


def old_bytes(path):
    return subprocess.check_output(['git', '-c', 'core.longpaths=true', 'show', f'{INTAKE}:{path}'], cwd=ROOT)


def old(path):
    return json.loads(old_bytes(path))


def sha(data):
    return 'sha256:' + hashlib.sha256(data).hexdigest()


def write(path, data):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')


def uri(path, commit='codex/salgado-accession'):
    return f'https://github.com/6529-Collections/6529networkmuseum/blob/{commit}/{path}'


def seal(path, p):
    p.update(record_status='review_pending', review_status='pending_independent_review', reviewer=None)
    r = m.finalize(p, path, False, None)
    r['envelope']['subjectId'] = m.keccak256(f"6529networkmuseum.subject.{p['record_type'].lower()}.v1:{p['subject_id']}".encode())
    r['envelope']['uri'] = uri(path)
    write(path, r)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--at', required=True, help='Actual UTC admission construction time')
    args = parser.parse_args()
    at = args.at
    certificate_path = ROOT / BASE / 'accession-certificate.json'
    if certificate_path.exists():
        raise SystemExit('Admission already constructed; preserve it and make a separate dated amendment.')
    receipt_path = 'notes/wip/2026-09-13-salgado-commit-review-receipt.json'
    receipt = json.loads((ROOT / receipt_path).read_bytes())
    verify_intake_approval(receipt)
    custody = old('evidence/salgado-amazonia-custody/summary.json')
    lot = old(BASE + '/accession-statement.json')['payload']
    accepted_at = lot['acceptance_date']
    title_path = BASE + '/public/title-rights-and-display.md'
    title_hash = sha(old_bytes(title_path))
    cref = deepcopy(lot['evidence_refs'][0])
    tref = {'label': 'Unrestricted gift and Museum title/display determination, reviewed intake edition',
            'uri': uri(title_path, INTAKE), 'sha256': title_hash, 'evidence_class': 'B', 'observed_at': accepted_at}
    rref = {'label': 'Independent Ultra review bound to the exact intake commit',
            'uri': uri(receipt_path), 'sha256': sha((ROOT / receipt_path).read_bytes()), 'evidence_class': 'B', 'observed_at': at}
    amendment_path = EVIDENCE + '/admission-amendment.json'
    amendment = {'amendment_id': LOT + '.AMENDMENT-20260913-01', 'observed_at': at,
                 'source_commit': INTAKE, 'constructor_id': ACTOR,
                 'basis': 'User-authorized unrestricted gift; adopted exact Museum Wave proposal; independently reviewed intake and catalogue.',
                 'reviewer_kind': 'independent_ai_agent',
                 'review_receipt': receipt_path,
                 'reason': 'Supersedes the intake-only current view with the formal accession act. Earlier receipts, observations, rights boundaries and source bytes remain unchanged.',
                 'superseded_records': []}
    paths = [BASE + '/accession-statement.json', BASE + '/gift-acceptance-authorization.json']
    paths += [f'{BASE}/{folder}/{name}.json' for folder, name in
              [(folder, (LOT + '.RIGHTS.' + f'{i:02d}') if folder == 'rights' else LOT + f'.{i:02d}')
               for folder in ['objects', 'rights', 'technical'] for i in range(1, 7)]]
    for path in paths:
        p = old(path)['payload']
        amendment['superseded_records'].append({'path': path, 'prior_version': p['record_version'],
            'supersedes': p['payload_sha256'], 'prior_raw_sha256': sha(old_bytes(path)),
            'prior_uri': uri(path, INTAKE)})
    write(amendment_path, amendment)
    aref = {'label': 'Dated admission amendment with immutable intake predecessors', 'uri': uri(amendment_path),
            'sha256': sha((ROOT / amendment_path).read_bytes()), 'evidence_class': 'B', 'observed_at': at}
    bindings = []
    for path in paths:
        p = old(path)['payload']
        p.update(record_version='1.1.0', observed_at=at, effective_at=at)
        for evidence in p['evidence_refs']:
            if evidence.get('uri', '').endswith('/public/title-rights-and-display.md'):
                evidence['uri'] = uri(title_path, INTAKE)
        p['evidence_refs'] += [rref, aref]
        if CERT not in p['references']:
            p['references'].append(CERT)
        if '/objects/' in path:
            p['current_state'] = 'technically_verified'
            for state in ['accessioned', 'catalogued', 'technically_verified']:
                p['state_history'].append({'state': state, 'observed_at': at, 'evidence_refs': [CERT]})
            p['state_history_semantics'] = 'The original four intake observations are unchanged. The later three states record admission and recognition of the independently reviewed catalogue and technical assessment at this amendment time.'
            p['condition']['narrative'] = 'Readable, fixity-verified source manifestation. Both regional source archives passed restoration and all 18 display copies rebuilt identically. Independent intake review is approved. The final admission/publication edition requires a subsequent archive capture.'
            p['uncertainties'] = [x for x in p['uncertainties'] if x != 'Accession record and scholarship await independent review.']
            bindings.append(deepcopy(p['title_binding']))
        elif path.endswith('gift-acceptance-authorization.json'):
            p['institutional_decision_authority'].update(documentation_qa_status='reviewed',
                publication_semantics='The reviewed gift acceptance is followed by accession certificate 6529NM-ACC-2026-004. GitHub publication review is a separate control.')
            p['completion_boundary'].update(current_state='accessioned', accession_status='complete', external_work_accession_certificate='executed', independent_review='reviewed', rights='reviewed_with_conditions', condition='reviewed_pass_with_conditions')
            p['completion_blockers'] = []
            p['non_claims'] = ['Copyright assignment is not recorded.', 'No general third-party reuse licence is granted.', 'Final publication and any production website deployment are separate from admission.']
        elif path.endswith('accession-statement.json'):
            p.update(accession_status='complete', intake_status='accessioned', remaining_gates=[],
                non_claims=['An unrestricted token gift does not transfer the artist copyright.', 'Preservation of the source package and archival capture of later publication editions have distinct scopes.'])
            p['ongoing_stewardship_actions'] = [
                {'action': 'Archive the final reviewed admission and publication edition with its commit and review receipts.', 'status': 'pending_final_edition', 'priority': 'high'},
                {'action': 'Maintain source fixity, recoverable copies, credited full-frame display and dated custody/control observations.', 'status': 'ongoing', 'priority': 'normal'}]
        seal(path, p)
    base = old('records/accessions/6529NM.2026.003/accession-certificate.json')['payload']
    certificate = {k: deepcopy(base[k]) for k in ['record_type', 'schema_id', 'visibility']}
    certificate.update(record_id=CERT, subject_id=LOT, record_version='1.0.0', created_at=at, observed_at=at, effective_at=at,
        constructor={'id': ACTOR, 'role': 'constructor', 'observed_at': at},
        accession_number=LOT, acquiring_institution='6529 Network Museum', acquisition_method='donation', acceptance_date=accepted_at,
        object_ids=lot['object_ids'], title_bindings=bindings, references=[LOT, GAA, WAVE, *lot['object_ids']],
        evidence_refs=[cref, tref, rref, aref], source={'source_record_ids': [LOT, GAA, WAVE], 'reviewed_intake_commit': INTAKE},
        review_outcomes={'institutional_authority': 'Adopted exact proposal and user-authorized unrestricted gift.',
            'identity_and_custody': 'Six exact tokens verified at finalized block 25971024.',
            'title': 'Executed donor declaration and Museum title determination bound to the exact six transfer logs.',
            'provenance': 'Continuous indexed mint-to-Museum transfers independently matched to 25 successful receipts.',
            'rights': 'Ordinary credited Museum use; creative-derivative and AI-training rights remain unspecified.',
            'condition_and_technical': 'Pass with documented metadata authority and retrieval dependencies.',
            'curatorial': 'Approved group study, artist and project studies, acquisition narrative and six individual entries.',
            'preservation': 'Two regional source copies restored and 18 derivatives reproduced from each; later edition capture remains an ongoing action.',
            'display': 'Ready with ordinary attribution, full-frame presentation and accessible descriptions.',
            'independent_review': 'User-appointed Ultra AI reviewer; exact 70-file intake commit approval. Final admission amendment review is recorded separately.'},
        ongoing_stewardship_actions=['Archive the final reviewed admission/publication edition.', 'Maintain fixity and regional recovery checks.', 'Maintain credited full-frame display, accessibility, custody and metadata-authority observations.'])
    certificate['events'] = [
        {'event_type': 'receipt', 'event_name': 'six_token_delivery', 'occurred_at': '2026-09-13T20:15:35Z', 'authority_reference': GAA, 'evidence_refs': [cref]},
        {'event_type': 'acceptance', 'event_name': 'formal_gift_acceptance', 'occurred_at': accepted_at, 'authority_reference': GAA, 'evidence_refs': [tref]},
        {'event_type': 'acquisition', 'event_name': 'unrestricted_donation_acquisition', 'occurred_at': accepted_at, 'authority_reference': GAA, 'evidence_refs': [tref]},
        {'event_type': 'title_passage', 'event_name': 'institutional_title_registration', 'occurred_at': accepted_at, 'authority_reference': GAA, 'evidence_refs': [tref],
         'instrument': {'kind': 'institutional_gift_title_declaration', 'reference': GAA, 'sha256': title_hash, 'uri': uri(title_path, INTAKE), 'custodian_reference': 'networkmuseum.6529.eth'}},
        {'event_type': 'custody_receipt', 'event_name': 'institutional_custody_registration', 'occurred_at': accepted_at, 'source_occurred_at': '2026-09-13T20:15:35Z',
         'event_semantics': 'Administrative registration after finalized verification; the source receipt time remains distinct.', 'authority_reference': GAA, 'evidence_refs': [cref],
         'custody_paths': [{'kind': 'onchain_token', 'object_id': x['object_id'], 'from': custody['donor_address'], 'to': custody['museum_address'], 'custodian_reference': 'networkmuseum.6529.eth'} for x in custody['objects']]},
        {'event_type': 'accession', 'event_name': 'permanent_collection_accession', 'occurred_at': at, 'authority_reference': CERT, 'evidence_refs': [rref, aref]}]
    seal(BASE + '/accession-certificate.json', certificate)
    register_path = 'records/accessions/register.json'
    register_raw = old_bytes(register_path)
    snapshot_path = EVIDENCE + '/register-revision-5.json'
    (ROOT / snapshot_path).write_bytes(register_raw)
    register = json.loads(register_raw)
    prior_hash = sha(m.canonicalize({k: v for k, v in register.items() if k != 'record_control'}))
    register['amendment_history'].append({'revision': 5, 'superseded_at': at, 'supersedes': prior_hash, 'prior_payload_sha256': prior_hash,
        'prior_source_commit': INTAKE, 'prior_snapshot_path': snapshot_path,
        'reason': 'Append the independently reviewed Salgado six-work gift. Revision five was constructed with no recorded reviewer; its exact source snapshot is preserved without inventing a prior review.'})
    register.update(snapshot_at=at, record_control={'revision': 6, 'record_status': 'constructed', 'constructor': {'actor_id': ACTOR, 'role': 'constructor', 'constructed_at': at}, 'review': None})
    register['lots'].append({'accession_lot_id': LOT, 'preferred_title': 'Amazônia: Forest, Water, and Community', 'object_count': 6,
        'donation_status': 'formally_accepted', 'accession_status': 'accessioned', 'formal_acceptance_status': 'formally_accepted',
        'gift_acceptance_authorization_record': GAA, 'accession_certificate_record': CERT, 'donor_public_credit': 'Gift of punk6529',
        'custody': {'ens': 'networkmuseum.6529.eth', 'chain_id': 'eip155:1', 'address': custody['museum_address'], 'observed_at': custody['completed_at'],
            'finalized_block': custody['finalized_block']['number'], 'finalized_block_hash': custody['finalized_block']['hash'], 'token_count': 6, 'evidence_class': 'A'},
        'receipt_event': {'transaction_hash': custody['objects'][0]['tx_hash'], 'block_number': 25970845, 'block_time': '2026-09-13T20:15:35Z',
            'from': custody['donor_address'], 'to': custody['museum_address'], 'transfer_count': 6, 'receipt_status': '0x1', 'evidence_class': 'A'},
        'evidence_refs': [BASE + '/accession-certificate.json', BASE + '/public/README.md', amendment_path],
        'completion_limits': [], 'ongoing_stewardship_actions': certificate['ongoing_stewardship_actions']})
    write(register_path, register)
    write(EVIDENCE + '/manifest.json', {'hash_algorithm': 'sha256', 'byte_mode': 'raw', 'entries': [
        {'path': Path(path).name, 'sha256': sha((ROOT / path).read_bytes()).removeprefix('sha256:'), 'size': (ROOT / path).stat().st_size, 'media_type': 'application/json'}
        for path in [amendment_path, snapshot_path]]})
    print('Admission amendment constructed; no independent approval metadata supplied.')


if __name__ == '__main__':
    main()
