"""Construct the Salgado intake records from retained evidence; never self-approve."""
from copy import deepcopy
from datetime import UTC, datetime
import hashlib, json
from pathlib import Path
import migrate_public_entities as m

ROOT=Path(__file__).resolve().parents[1]
LOT='6529NM.2026.004'; PG='6529NM-PG-2026-003'; GAA=LOT+'.GAA-01'; WAVE='6529NM-WAVE-OBS-2026-09-13-003'
ACTOR='codex-task:01a087a1-5e64-7280-b5f8-82d0df4ec066'
BASE=f'records/accessions/{LOT}'
def load(p):return json.loads((ROOT/p).read_bytes())
def write(p,value):
 target=ROOT/p;target.parent.mkdir(parents=True,exist_ok=True)
 target.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def sha(p):return 'sha256:'+hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def uri(p):return 'https://github.com/6529-Collections/6529networkmuseum/blob/codex/salgado-accession/'+p
cust=load('evidence/salgado-amazonia-custody/summary.json')
sources=load('evidence/salgado-amazonia-sources/manifest.json')
prov=load('evidence/salgado-amazonia-provenance/summary.json')
wave=load('evidence/salgado-amazonia-wave/response.json')
wm=load('evidence/salgado-amazonia-wave/manifest.json')
restoration=load('evidence/salgado-amazonia-preservation/restoration-summary.json')
screening=load('evidence/salgado-amazonia-diligence/ofac-address-screening.json')
AT=sources['observed_at']; WAVETIME=wm['completed_at']
assert wave['id']=='4eeb759a-74e8-43b6-a155-f9b015f003df' and wave['serial_no']==1344468 and wave['drop_type']=='WINNER'
assert [x['token_id'] for x in cust['objects']]==[226,1117,2059,2216,2768,4697]
def ref(label,path,kind='A',at=AT):return {'label':label,'uri':uri(path),'evidence_class':kind,'observed_at':at,'sha256':sha(path)}
CREF=ref('Finalized custody and exact transfer receipts','evidence/salgado-amazonia-custody/summary.json',at=cust['completed_at'])
SREF=ref('Source JPEG and metadata characterization','evidence/salgado-amazonia-sources/manifest.json','C')
PREF=ref('Mint-to-Museum indexed transfer receipt verification','evidence/salgado-amazonia-provenance/summary.json',at=prov['completed_at'])
WREF=ref('Authenticated exact proposal readback','evidence/salgado-amazonia-wave/response.json','B',WAVETIME)
TREF=ref('Donor declaration and Museum display determination',BASE+'/public/title-rights-and-display.md','B')
RREF=ref('Two regional source-package restoration tests','evidence/salgado-amazonia-preservation/restoration-summary.json','C',restoration['completed_at'])
DREF=ref('Official OFAC exact-address UI observations','evidence/salgado-amazonia-diligence/ofac-address-screening.json','B',screening['observed_at'])
REFS=[CREF,SREF,PREF,WREF,TREF,RREF,DREF]
def common(template,rid,subject=None):
 p=deepcopy(template)
 p.update(record_id=rid,subject_id=subject or rid,created_at=AT,observed_at=screening['observed_at'],effective_at=AT,
 constructor={'id':ACTOR,'role':'constructor','observed_at':AT},reviewer=None,
 record_status='review_pending',review_status='pending_independent_review',record_version='1.0.1',
 payload_sha256='sha256:'+'0'*64,references=[GAA,WAVE],evidence_refs=deepcopy(REFS))
 p['source']={'source_record_ids':[GAA,WAVE]}
 return p
def seal(path,p):
 record=m.finalize(p,path,False,None)
 record['envelope']['subjectId']=m.keccak256(f"6529networkmuseum.subject.{p['record_type'].lower()}.v1:{p['subject_id']}".encode())
 record['envelope']['uri']=uri(path)
 write(path,record)

oldwave=load('records/proposed-gifts/6529NM-PG-2026-002/wave-status-observation.json')['payload']
wp=common(oldwave,WAVE)
wp['prior_observation']={'source_status':'PARTICIPATORY','observed_at':'2026-08-25T21:56:48.461Z','source_record_id':PG,'source_record_path':None,'source_repository_visibility':'complete_manifest_only','source_url':'https://6529.io/waves/5f207393-5418-4a75-8738-e40edb44a94d?drop='+wave['id']}
wp.update(observation_id=WAVE,proposal_id=PG,wave_id=wave['wave']['id'] if isinstance(wave.get('wave'),dict) else '5f207393-5418-4a75-8738-e40edb44a94d',
 drop_id=wave['id'],serial_no=wave['serial_no'],drop_type=wave['drop_type'],source_status=wave['drop_type'],
 api_reported_is_signed=wave['is_signed'],source_url='https://6529.io/waves/5f207393-5418-4a75-8738-e40edb44a94d?drop='+wave['id'],
 rating=wave['rating'],realtime_rating=wave['realtime_rating'],rater_count=wave['raters_count'] if 'raters_count' in wave else wave['rater_count'],
 observed_at=WAVETIME,effective_at=WAVETIME,source_record_ids=[PG],references=[PG],evidence_refs=[WREF],source={'source_record_ids':[PG]})
seal(f'records/proposed-gifts/{PG}/wave-status-observation.json',wp)

templates={name:load(path)['payload'] for name,path in {
 'object':'records/accessions/6529NM.2026.002/objects/6529NM.2026.002.01.json',
 'rights':'records/accessions/6529NM.2026.002/rights/6529NM.2026.002.RIGHTS.01.json',
 'condition':'records/accessions/6529NM.2026.002/technical/6529NM.2026.002.01.json',
 'gaa':'records/accessions/6529NM.2026.003/gift-acceptance-authorization.json',
 'lot':'records/accessions/6529NM.2026.003/accession-statement.json'}.items()}
assets=[]
for co,so,po in zip(cust['objects'],sources['objects'],prov['objects']):
 assert co['token_id']==so['token_id']==po['token_id']
 oid=co['object_id'];suffix=oid.rsplit('.',1)[1];token=co['token_id']
 title=(ROOT/f'{BASE}/public/{oid}.md').read_text(encoding='utf8').splitlines()[0][2:]
 titlebinding={'object_id':oid,'status':'executed','instrument_sha256':TREF['sha256'],'custodian_reference':'networkmuseum.6529.eth',
  'transfer_transaction':co['tx_hash'],'block_number':co['block_number'],'from':cust['donor_address'],'to':cust['museum_address'],'bound_at':AT,
  'basis':'Unrestricted donor declaration and authorized Museum acceptance, corroborated by delivery of the exact token. Copyright remains separate.'}
 rights={}
 for use in ['reproduction','publication','exhibition','print','derivative_use','ai_training','preservation','migration_emulation','accessibility']:
  normal=use in ['reproduction','publication','exhibition','print','preservation','accessibility']
  rights[use]={'grant_status':'granted_with_conditions' if normal else 'not_applicable' if use=='migration_emulation' else 'unspecified',
   'observed_at':AT,'evidence_ref':GAA,'basis':
   'Museum use determination: ordinary credited exhibition, catalogue, education, documentation and faithful technical copies for care. No general third-party licence or copyright transfer.'
   if normal else 'No emulation is needed for these static JPEGs.' if use=='migration_emulation' else 'No general creative-derivative or model-training licence is asserted; faithful display transformations are covered by ordinary Museum use.'}
 cond={'token':'green','metadata':'green','script':'not_applicable','dependencies':'amber','rendering':'green','behavior':'not_applicable','documentation':'amber',
  'protocol_state':'Static JPEG associated with Ethereum ERC-721; mutable metadata authority and gateway retrieval dependencies recorded separately.',
  'method':'Exact receipt/log and pinned finalized custody; source hash matching, full JPEG decode, ICC/geometry characterization and full-frame visual examination.',
  'narrative':'Readable, fixity-verified source manifestation. Both regional source archives passed restoration and all 18 display copies rebuilt identically. Binding Museum review and archival capture of the final publication edition remain pending.',
  'observed_at':restoration['completed_at']}
 obj=common({},oid)
 obj.update(record_type='WORK_DESCRIPTION',schema_id=templates['object']['schema_id'],visibility='public',
  object_id=oid,accession_lot_id=LOT,title=title,creator='Sebastião Salgado',medium='Black-and-white digital photograph; JPEG associated with an ERC-721 token',
  credit_line='Gift of punk6529. Photograph © Sebastião Salgado.',current_state='received_onchain',
  chain_identity={'caip19':co['caip19'],'chain_id':1,'contract':co['contract'],'token_id':str(token),'token_standard':'ERC-721',
    'mint_transaction':po['transfers'][0]['tx_hash'],'acquisition_transaction':co['tx_hash'],
    'custody_receipt_transaction':co['tx_hash'],'custody_receipt_block':co['block_number'],'custody_receipt_log':co['log_index'],
    'custody_account':'eip155:1:'+cust['museum_address'],'custody_status':'verified','custody_verified_at':cust['completed_at'],
    'custody_block':cust['finalized_block']['number'],'metadata_uri':co['token_uri'],'metadata_sha256':so['metadata']['sha256']},
  title_binding=titlebinding,rights=rights,condition=cond,
  state_history=[{'state':'offered','observed_at':'2026-08-25T21:56:48.461Z','evidence_refs':[PG]}, {'state':'authorized','observed_at':AT,'evidence_refs':[WAVE,GAA]}, {'state':'acquired','observed_at':AT,'evidence_refs':[GAA]}, {'state':'received_onchain','observed_at':AT,'evidence_refs':[GAA,WAVE]}],
  state_history_semantics='The receipt occurred at 2026-09-13T20:15:35Z; this state records subsequent finalized verification. Admission awaits independent review and an executed accession certificate.',
  preservation={'status':'in_progress','package_uri':RREF['uri'],'fixity_sha256':RREF['sha256'],
    'render_environment':'Source preservation complete for the captured scope: two private regional copies restored, all 341 files verified, all 18 WebP copies reproduced identically with Pillow 12.3.0 and archived transform code. The final reviewed publication edition still requires archival capture.','observed_at':restoration['completed_at']},
  display={'status':'ready_with_conditions','manifest_uri':uri(BASE+'/public/display-and-preservation.md'),'credit_line':'Gift of punk6529. Photograph © Sebastião Salgado.','observed_at':AT},
  artist={'claim_type':'source_credit','evidence_class':'B','preferred_name':'Sebastião Salgado','source_refs':[PG]},
  evidence_grade='A/B/C/E',source_refs=[PG,GAA,WAVE],
  uncertainties=['Issuer date-code suffix is not established as a calendar month.','The source JPEG is a finished edition manifestation; camera originals are not held.',
   'Specific book/exhibition appearance of this exact image is not established.','Accession record and scholarship await independent review.'])
 seal(f'{BASE}/objects/{oid}.json',obj)
 rp=common(templates['rights'],LOT+'.RIGHTS.'+suffix)
 rp.update(object_id=oid,rights_holder_reference='Sebastião Salgado / applicable rights holders; no transfer of copyright recorded',
  basis='Unrestricted gift and ordinary Museum display determination; donor imposes no restrictions. Existing copyright and attribution remain separate.',grants=rights,
  events=[{'event_id':LOT+'.RIGHTS.'+suffix+'.EVENT.01','event_type':'rights_assertion','occurred_at':AT,'authority_reference':GAA,'evidence_refs':[TREF]}])
 seal(f'{BASE}/rights/{LOT}.RIGHTS.{suffix}.json',rp)
 cp=common(templates['condition'],LOT+'.COND.'+suffix)
 cp.update(object_id=oid,protocol_state=cond['protocol_state'],assessments={k:cond[k] for k in ['token','metadata','script','dependencies','rendering','behavior','documentation']},
 method=cond['method'],outcome=cond['narrative'],events=[{'event_id':LOT+'.COND.'+suffix+'.EVENT.01','event_type':'condition_assessment','occurred_at':AT,'authority_reference':GAA,'evidence_refs':[CREF,SREF]}, {'event_id':LOT+'.COND.'+suffix+'.EVENT.02','event_type':'condition_assessment','occurred_at':restoration['completed_at'],'authority_reference':GAA,'evidence_refs':[RREF]}])
 seal(f'{BASE}/technical/{oid}.json',cp)
 assets.append({'object_id':oid,'title':title,'caip19':co['caip19'],'contract':co['contract'],'token_id':str(token),'custody_receipt_log':co['log_index']})

gaa=common(templates['gaa'],GAA,LOT)
basis=deepcopy(templates['gaa']['governing_basis'][0])
basis.update(decision_id=WAVE,drop_id=wave['id'],governance_record_ref=WAVE,live_api_observed_at=WAVETIME,observed_at=WAVETIME,
 source_uri=wp['source_url'],title='Proposed gift: Sebastião Salgado, Amazônia',wave_serial=1344468)
gaa.update(authorization_id=GAA,formal_acceptance_date=AT,assets=assets,governing_basis=[basis],
 permanent_collection_intent='The Museum accepts the exact six-work unrestricted gift for permanent Collection accession processing. The group is the gift decision unit, without a perpetual joint-display condition.',
 consideration={'status':'none','statement':'The donor gives these six tokenized objects without consideration.'},
 donor_authority_declaration={'source_type':'user_supplied_donor_and_authority_fact',
  'statement':'punk6529 directly confirms donor identity and an unrestricted gift; ordinary Museum display and care are authorized. No further donor rights information is required.',
  'authentication':'Direct instruction in the Salgado Accession task, corroborated by the adopted exact proposal and successful donor-to-Museum delivery.',
  'limitations':['Donor title and artist copyright are separate.','No general third-party licence is created.','The declaration does not identify unnamed photographic subjects.']},
 custody_receipts=[{'transaction_hash':cust['objects'][0]['tx_hash'],'block_number':25970845,'block_time':'2026-09-13T20:15:35Z',
  'from':cust['donor_address'],'to':cust['museum_address'],'custody_ens':'networkmuseum.6529.eth','transfer_count':6,'receipt_status':'0x1',
  'logs':[{'object_id':x['object_id'],'log_index':x['log_index']} for x in cust['objects']]}],
 institutional_decision_authority={'authority_basis':'user_authorized_institutional_decision','decision_status':'formally_accepted',
  'documentation_qa_status':'pending_independent_review','effective_at':AT,
  'publication_semantics':'Authorized gift acceptance and accession processing; this constructed record does not execute the accession certificate or claim public release.'},
 completion_boundary={'current_state':'received_onchain','accession_status':'not_complete','external_work_accession_certificate':'pending',
 'independent_review':'pending','preservation':'in_progress','rights':'pending','condition':'pending','title_binding':'executed'},
 completion_blockers=['independent_review','execute_accession_certificate_after_review'],
 non_claims=['Copyright assignment is not recorded.','No general third-party reuse licence is granted.','Independent review and accession admission have not occurred.'])
gaa['references']=[WAVE,*[x['object_id'] for x in assets]];gaa['source']={'source_record_ids':[WAVE]}
seal(f'{BASE}/gift-acceptance-authorization.json',gaa)

lot=common(templates['lot'],LOT)
lot.update(acceptance_date=AT,formal_acceptance_date=AT,accession_number=LOT,accession_status='not_complete',intake_status='accepted_for_accession_processing',
 gift_acceptance_authorization_record=GAA,object_ids=[x['object_id'] for x in assets],governing_references=[GAA,WAVE],
 remaining_gates=['independent_review','execute_accession_certificate_after_review'],non_claims=['Unrestricted donor gift is separate from copyright ownership.','Identifiers are allocated for processing; permanent Collection admission is not yet asserted.'],
 preservation_manifest={'status':'in_progress','manifest_sha256':SREF['sha256'],'fixity_sha256':SREF['sha256'],'manifest_uri':SREF['uri'],
 'objects':[{'object_id':x['object_id'],'metadata_uri':x['metadata']['uri'],'metadata_sha256':x['metadata']['sha256'],'metadata_raw_path':x['metadata']['path']} for x in sources['objects']],
 'raw_metadata_status':'retained','raw_generator_status':'not_applicable_static_photographs',
 'active_stewardship_actions':['Preserve source JPEG and metadata bytes with independently recoverable copies and a documented restoration.','Maintain source fixity, credited display and metadata-authority observations.']})
lot['references']=[GAA,WAVE,*lot['object_ids']]
lot.pop('preservation_manifest',None)
seal(f'{BASE}/accession-statement.json',lot)
print(f'Constructed 21 typed records for {LOT}; all independent reviews remain pending.')
