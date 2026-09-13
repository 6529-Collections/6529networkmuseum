"""Salgado's independently reviewed projection, separate from earlier review scopes."""
from pathlib import Path

ACTOR = 'codex-task:01a087a1-5e64-7280-b5f8-82d0df4ec066'
LOT = '6529NM.2026.004'
BASE = f'records/accessions/{LOT}'
ARTIST = '6529NM-ART-0024'
PROJECT = '6529NM-PRJ-0008'
GROUP = '6529NM-CA-2026-005'
ACCESSION = '6529NM-ACC-ENT-0004'
PUBLICATION = '6529NM-RP-0004'
CERT = '6529NM-ACC-2026-004'
GAA = LOT + '.GAA-01'
WORKS = [f'6529NM-W-{i:04d}' for i in range(30, 36)]
MEDIA = [f'6529NM-MED-{i:04d}' for i in range(54, 60)]
TITLE = 'Amazônia: Forest, Water, and Community'


def add_records(m, records, relation_indexes, used_relation_keys, identity_inventory, review_arguments=None):
    """Append one review scope without changing any earlier review binding."""
    args = review_arguments or {'reviewed': False, 'reviewer_id': None}
    certificate = m.load_json(m.ROOT / BASE / 'accession-certificate.json')['payload']
    at = certificate['created_at']
    sources = m.load_json(m.ROOT / 'evidence/salgado-amazonia-sources/manifest.json')
    media = m.load_json(m.ROOT / 'evidence/salgado-amazonia-preservation/display-preparation.json')
    institution = '6529NM-I-0001'
    collection = '6529NM-C-0001'
    program = '6529NM-AP-ENT-0001'
    references = [LOT, CERT, GAA]

    def ev(label, path, kind='B'):
        return {'label': label, 'uri': f'https://github.com/6529-Collections/6529networkmuseum/blob/main/{path}',
                'sha256': m.sha256_file(m.ROOT / path), 'observed_at': at, 'evidence_class': kind}

    ce = ev('Salgado accession certificate', BASE + '/accession-certificate.json')
    ge = ev('Unrestricted gift acceptance', BASE + '/gift-acceptance-authorization.json')
    se = ev('Source image and metadata characterization', 'evidence/salgado-amazonia-sources/manifest.json', 'C')
    pe = ev('Two regional source-package restoration tests', 'evidence/salgado-amazonia-preservation/restoration-summary.json', 'C')
    re = ev('Museum display and rights determination', BASE + '/public/title-rights-and-display.md')
    essay = ev('Collection essay', BASE + '/public/forest-water-and-community.md', 'E')

    def finish(relative, payload):
        if relative in records:
            raise ValueError(f'Duplicate Salgado projection path: {relative}')
        payload.update(created_at=at, constructor={'id': ACTOR, 'role': 'constructor', 'observed_at': at})
        records[relative] = m.finalize(payload, relative, **args)

    def entity(eid, kind, label, slug, route, profile, refs, evidence, media_ids=None):
        relative, payload = m.entity(eid, kind, label, slug, route, at, profile, refs, evidence,
                                    reviewed=args.get('reviewed', False), media_entity_ids=media_ids)
        finish(relative, payload)

    def relation(kind, source, target, evidence, qualifier=None):
        qualifier = qualifier or {}
        key = m.semantic_relation_key(kind, source, target, qualifier)
        if key in used_relation_keys or key not in relation_indexes:
            raise ValueError(f'Missing or repeated Salgado relation binding: {key}')
        used_relation_keys.add(key)
        relative, payload = m.relation(relation_indexes[key], kind, source, target, qualifier, at, references, evidence)
        finish(relative, payload)

    ae = ev('Sebastião Salgado artist study', BASE + '/public/sebastiao-salgado.md', 'E')
    entity(ARTIST, 'ARTIST', 'Sebastião Salgado', 'sebastiao-salgado', '/museum/network/artists/sebastiao-salgado',
        {'profile_type': 'ARTIST', 'authority': {'authority_status': 'established', 'authority_record_ids': [], 'evidence_refs': [ae, se]},
         'name_variants': [{'value': 'Sebastião Salgado', 'variant_role': 'preferred', 'source_kind': 'published_source', 'evidence_refs': [se]}],
         'practice': {'summary': 'Salgado developed long photographic projects through travel, repeated visits and the sequencing of black-and-white photographs. Amazônia brings forest landscapes and Indigenous communities into that serial practice.',
                      'areas': ['photography', 'documentary photography', 'landscape'], 'evidence_refs': [ae]}}, references, [ae, se])
    pre = ev('Amazônia project study', BASE + '/public/amazonia-project.md', 'E')
    entity(PROJECT, 'PROJECT_OR_SERIES', 'Amazônia', 'amazonia', '/museum/network/projects/amazonia',
        {'profile_type': 'PROJECT_OR_SERIES', 'project_type': 'project', 'project_relation_basis': 'source_project_record',
         'agent_entity_ids': [ARTIST], 'work_entity_ids': WORKS, 'source_record_ids': references,
         'scope_statement': 'Amazônia is Salgado’s photographic project on the Amazon forest and its inhabitants. The Museum holds six images in the 2022 token edition, selected as a Museum group.',
         'ownership_boundary': 'The Museum group is one selection from Amazônia; it does not define the artist’s project or sequence.', 'evidence_refs': [pre, se]}, references + [ARTIST], [pre, se])
    facts = {}
    fact_specs = {
        'mint': ('verified', 'The tokens were minted in 2022 before this gift.', ev('Mint-to-Museum receipt verification', 'evidence/salgado-amazonia-provenance/summary.json', 'A')),
        'payment': ('not_applicable', 'The six works were donated without consideration.', ge),
        'title': ('verified', 'The Museum records the donor’s transferable token interest separately from copyright.', ce),
        'custody': ('verified', 'The six tokens were verified at finalized Ethereum block 25971024.', ev('Finalized custody', 'evidence/salgado-amazonia-custody/summary.json', 'A')),
        'rights': ('verified_with_conditions', 'Ordinary credited Museum use is recorded; no general third-party reuse licence is asserted.', re),
        'technical': ('verified_with_conditions', 'The JPEGs decode and display; mutable metadata authority and retrieval dependencies remain documented.', se),
        'preservation': ('in_progress', 'Both source archives passed restoration; subsequent publication editions are retained through separate captures.', pe),
        'display': ('verified_with_conditions', 'Full-frame, credited and accessible Museum presentation is ready.', re)}
    for name, (status, note, evidence) in fact_specs.items():
        facts[name] = {'status': status, 'as_of': at, 'notes': note, 'evidence_refs': [evidence]}
    for i, (wid, mid, source, display) in enumerate(zip(WORKS, MEDIA, sources['objects'], media['items']), 1):
        oid = LOT + f'.{i:02d}'
        obj = m.load_json(m.ROOT / BASE / 'objects' / (oid + '.json'))['payload']
        oe = ev('Individual object entry', BASE + '/public/' + oid + '.md', 'E')
        title = obj['title']
        # The recorded caption year is distinct from the NFT release year.
        import re as regex
        text = (m.ROOT / BASE / 'public' / (oid + '.md')).read_text(encoding='utf8')
        year = regex.search(r'\*\*Date:\*\* (\d{4})', text).group(1)
        entity(wid, 'WORK', title, wid, '/museum/network/works/' + wid,
            {'profile_type': 'WORK', 'title': title, 'creator_entity_ids': [ARTIST],
             'creation_date': {'display': year, 'status': 'established', 'earliest': year + '-01-01', 'latest': year + '-12-31', 'evidence_refs': [oe, se]},
             'medium': obj['medium'], 'work_lifecycle_status': 'accessioned',
             'current_museum_relation': {'museum_entity_id': institution, 'relation_status': 'permanent_collection', 'as_of': at, 'evidence_refs': [ce]},
             'mint_fact': facts['mint'], 'collection_membership': {'status': 'permanent_collection', 'collection_entity_id': collection, 'accession_entity_ids': [ACCESSION], 'source_record_ids': [LOT, CERT], 'evidence_refs': [ce]},
             'project_or_series_entity_ids': [PROJECT], 'acquisition_entity_ids': [GROUP], 'program_entity_ids': [program], 'accession_entity_ids': [ACCESSION],
             'lifecycle_observations': [m.lifecycle_observation(f'6529NM-W-OBS-{39+i:04d}', 'accessioned_into_permanent_collection', 'accessioned', at, [CERT, oid], 'Admitted through the reviewed six-work unrestricted gift.', [ce])],
             'component_references': [m.authoritative_typed_reference('component', oid, 'WORK_DESCRIPTION', [ce])],
             'manifestation_references': [m.governed_typed_reference(identity_inventory, 'manifestation', oid + '.TOKEN', oid, [se], source_status='verified')],
             'identity_boundary': 'Photographic image, token, Museum title, copyright and accession are distinct records.', 'evidence_refs': [oe, ce, se]},
             references + [oid, ARTIST, PROJECT, GROUP, ACCESSION], [oe, ce, se], [mid])
        derivative = next(x for x in display['derivatives'] if x['width'] == 1280)
        image_path = 'media/accessions/' + LOT + '/' + derivative['filename']
        digest = m.sha256_file(m.ROOT / image_path)
        if digest != derivative['sha256']:
            raise ValueError(f'Salgado media fixity mismatch: {image_path}')
        profile = m.media_profile('museum_generated_public_derivative', None, image_path, 'image/webp', True, derivative['width'], derivative['height'],
            display['accessibility_text'], 'provided', wid, obj['credit_line'], 'cleared_with_conditions', 'retrieved', [oid, LOT + f'.RIGHTS.{i:02d}'], at,
            {'status': 'verified', 'algorithm': 'sha256', 'digest': digest, 'verified_at': at, 'basis': 'Byte-identical derivative regenerated independently from each restored regional source package.'},
            ['view', 'thumbnail', 'hero', 'alt_text', 'copy_citation'], source_byte_size=derivative['bytes'],
            transform='Full-frame Adobe RGB to fixed sRGB; Lanczos resize; WebP quality 82, method 6; EXIF/XMP stripped.',
            token_source_locator={'uri': source['image']['uri'], 'repository_path': None},
            token_source_fixity={'status': 'verified', 'algorithm': 'sha256', 'digest': source['image']['sha256'], 'verified_at': at, 'basis': 'Retained source JPEG verified against the approved source snapshot; no assertion about future gateway responses.'},
            rights_label='Credited Museum display', rights_evidence_refs=[re], source_observation_evidence_refs=[se, pe], accessibility_evidence_refs=[oe])
        entity(mid, 'MEDIA_REFERENCE', title + ' — Museum display copy', None, None, profile, references + [wid, oid], [se, pe, re])
        for predicate, source_id, target in [('ARTIST_CREATES_WORK', ARTIST, wid), ('PROJECT_CONTEXTUALIZES_WORK', PROJECT, wid), ('CURATED_ACQUISITION_BRINGS_TOGETHER_WORK', GROUP, wid), ('ACCESSION_ADMITS_WORK', ACCESSION, wid), ('COLLECTION_CONTAINS_WORK', collection, wid), ('ENTITY_HAS_MEDIA', wid, mid)]:
            qualifier = {'CURATED_ACQUISITION_BRINGS_TOGETHER_WORK': {'display_order': i},
                         'ACCESSION_ADMITS_WORK': {'accession_object_id': oid},
                         'COLLECTION_CONTAINS_WORK': {'collection_membership_status': 'permanent_collection'},
                         'ENTITY_HAS_MEDIA': {'media_context': 'primary'}}.get(predicate, {})
            relation(predicate, source_id, target, [ce, oe], qualifier)
    entity(ACCESSION, 'ACCESSION', 'Salgado accession ' + LOT, None, None,
        {'profile_type': 'ACCESSION', 'accession_number': LOT, 'accession_status': 'complete', 'admitted_work_entity_ids': WORKS, 'source_accession_record_id': LOT, 'evidence_refs': [ce]}, references + WORKS, [ce])
    entity(GROUP, 'CURATED_ACQUISITION', TITLE, 'forest-water-and-community', '/museum/network/acquisitions/forest-water-and-community',
        {'profile_type': 'CURATED_ACQUISITION', 'title': TITLE, 'thesis': 'Six photographs bring forest vegetation, ridges, clouds, river courses and Indigenous communities into a Museum selection from Amazônia.',
         'acquisition_method': 'donation', 'program_or_pathway': {'kind': 'acquisition_program', 'entity_ids': [program], 'source_record_ids': [GAA]},
         'work_entity_ids': WORKS, 'source_work_record_ids': certificate['object_ids'], 'collection_effect': 'permanent_collection',
         'lifecycle': {'status': 'accessioned_into_permanent_collection', 'as_of': at, 'evidence_refs': [ce]},
         'lifecycle_observations': [m.lifecycle_observation('6529NM-CA-OBS-0006', 'accessioned_into_permanent_collection', 'accessioned', at, [CERT, GAA], 'The independently reviewed six-work gift is admitted to the permanent Collection.', [ce])],
         'independent_acquisition_facts': facts, 'public_credit': 'Gift of punk6529', 'evidence_refs': [essay, ce, ge]}, references + WORKS + [program, ACCESSION], [essay, ce, ge])
    components = sorted(p.relative_to(m.ROOT).as_posix() for p in (m.ROOT / BASE / 'public').glob('*.md'))
    entity(PUBLICATION, 'RESEARCH_PUBLICATION', TITLE, 'forest-water-and-community', '/museum/network/research/forest-water-and-community',
        {'profile_type': 'RESEARCH_PUBLICATION', 'title': TITLE, 'publication_kind': 'research_dossier', 'publication_date': at[:10], 'version': '1.0.0',
         'publication_document_uri': essay['uri'], 'publication_component_paths': components, 'author_entity_ids': [institution],
         'subject_entity_ids': [GROUP, ARTIST, PROJECT, *WORKS], 'evidence_refs': [essay, ce]}, references + [GROUP, ARTIST, PROJECT, *WORKS], [essay, ce])
    relation('ACQUISITION_PROGRAM_PRODUCES_ACQUISITION', program, GROUP, [ge])
    relation('PUBLICATION_INTERPRETS_ENTITY', PUBLICATION, GROUP, [essay])
    relation('INSTITUTION_PUBLISHES_PUBLICATION', institution, PUBLICATION, [essay])
    relation('AGENT_PLAYS_ROLE', ARTIST, PROJECT, [pre], {'role': 'creator'})
    # Membership changes are new assertions in this review scope. The original
    # collection/program projection remains retrievable at the intake commit.
    for eid, field, additions in [(collection, 'admitted_work_entity_ids', WORKS),
                                  (program, 'produced_acquisition_entity_ids', [GROUP])]:
        path = f'records/entities/{eid}.json'
        payload = records.pop(path)['payload']
        payload['profile'][field] += additions
        payload['record_version'] = '1.1.0'
        payload['observed_at'] = at
        payload['effective_at'] = at
        payload['evidence_refs'] += [ce, {'label': 'Superseded membership projection, preserved intake commit',
            'uri': f'https://github.com/6529-Collections/6529networkmuseum/blob/4939941ae69d5edf0eec86712186add1666ab410/{path}',
            'observed_at': at, 'evidence_class': 'B'}]
        payload['references'] = sorted(set(payload['references'] + references))
        payload['source_record_ids'] = sorted(set(payload['source_record_ids'] + references))
        payload['profile']['evidence_refs'].append(ce)
        payload['reviewer'] = None
        payload['record_status'] = 'review_pending'
        payload['review_status'] = 'pending_independent_review'
        payload['entity_status'] = 'published' if args.get('reviewed') else 'review_pending'
        payload['status_observation'] = {'status_label': payload['entity_status'], 'observed_at': at, 'evidence_refs': [ce]}
        finish(path, payload)
