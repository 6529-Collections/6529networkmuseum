# CAIP-19: an address for a chain asset

Status: working Museum application profile; the cited standard remains authoritative

## The question

**Which exact asset, on which exact chain, does the Museum mean?**

“Token 42” is ambiguous. Thousands of contracts can issue a token 42, and the
same contract address can exist on different chains. CAIP-19 combines a chain
identifier, asset namespace, and contract or asset reference. Where applicable,
it also includes an individual token identifier.

For *CENTURY #31*, the Museum records:

```text
eip155:1/erc721:0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/100000031
```

Read from left to right: Ethereum's EIP-155 namespace, chain ID 1, the ERC-721
contract, and the token ID. It identifies the blockchain asset precisely; the
Museum still records the artwork and its collection object separately.

## What CAIP-19 contributes

The core specification defines:

```text
asset_type = chain_id "/" asset_namespace ":" asset_reference
asset_id   = asset_type "/" token_id
```

CAIP-2 supplies the chain identifier. Namespace profiles define the allowed
asset namespace, contract/reference syntax, and token identifier for a chain
family.

## Museum application profile

### Ethereum ERC-721 form

```text
eip155:<decimal chain id>/erc721:<lowercase 0x address>/<base-10 token id>
```

The Museum lowercases the contract address for canonical comparison and retains
the EIP-55 checksum form separately for display. Token IDs are base-10 strings
with no leading zero unless the value is zero. JSON stores token IDs as strings
to avoid loss above JavaScript's safe integer range.

These normalization rules are Museum rules. The core CAIP-19 grammar is
case-sensitive and does not impose this Ethereum canonicalization.

### Identity and observed state

The CAIP-19 string remains stable while custody, approval, metadata, token URI,
contract code, or lifecycle state changes. A separate chain observation records
chain ID, block number, block hash, canonicality/finality state, RPC request and
response, transaction or log, observation time, and evidence fixity.

The Museum does not append private suffixes such as `@finalized` to a CAIP-19
identifier. State belongs in the observation record and its digest.

### Contract-level and token-level identity

```text
eip155:1/erc721:0x...        contract-level asset type
eip155:1/erc721:0x.../42     individual token
```

An object record for one NFT requires the token-level form.

## Profile-status caveat

The relevant CAIP-19 documents are not all final. The core specification is
marked **Review**, and the EIP-155 asset namespace profile is marked **Draft**
with a withdrawal reason referring to CAIP-21 and CAIP-22. The Museum therefore
calls its current values “CAIP-19-shaped,” pins the documents it used, and
treats its lowercase/decimal form as a versioned Museum profile. Any later final
namespace will be compared before migration.

## What this standard leaves to the Museum

CAIP-19 identifies an asset string. It supplies no proof that the asset exists,
that a contract implements ERC-721 correctly, that the token is owned by the
Museum, that metadata is stable, that the artist authored the associated work,
or that the object was accessioned. It has no file fixity, block state,
signature, version history, rights, or preservation semantics.

## For machines and implementers

### Authority and status

- Core: [CAIP-19 Asset Type and Asset ID Specification](https://standards.chainagnostic.org/CAIPs/caip-19), status Review.
- Chain identity dependency: [CAIP-2](https://standards.chainagnostic.org/CAIPs/caip-2), status Final.
- Ethereum profile: [EIP-155 Namespace Assets](https://namespaces.chainagnostic.org/eip155/caip19), status Draft/withdrawn.
- Token interface: [ERC-721](https://eips.ethereum.org/EIPS/eip-721), Final.

### Closed Museum pattern

```regex
^eip155:[1-9][0-9]*/erc721:0x[0-9a-f]{40}/(0|[1-9][0-9]*)$
```

The profile separately checks that the token ID fits `uint256`, the chain ID is
the intended network, the contract contains code at the observation block, and
the observation evidence supports the declared token standard and state.

### Reproducible chain evidence

Where an RPC supports it, state reads use an EIP-1898 block selector:

```json
{
  "blockHash": "0x...",
  "requireCanonical": true
}
```

The Museum retains exact request and response bytes, selected block header,
contract code, interface checks, `ownerOf`, token approval, relevant receipts
and logs, token URI, metadata response, parser version, and derived values. The
CAIP-19 identifier joins those observations; it does not absorb them.

## The Casey Reas accession

Museum state: `source_fields_present`. All seven object records carry the Museum-normalized
token-level form and separate chain fields. CI validates internal contract/token
agreement and the evidence package verifies important receipt and custody
claims. Because the EIP-155 namespace profile is not final, the Museum describes
the values as CAIP-19-shaped and will include them in the later standards
convergence review.

## Official sources

- Chain Agnostic Standards Alliance, [CAIP-19](https://standards.chainagnostic.org/CAIPs/caip-19).
- Chain Agnostic Standards Alliance, [CAIP-2](https://standards.chainagnostic.org/CAIPs/caip-2).
- Chain Agnostic Namespaces, [EIP-155 asset profile](https://namespaces.chainagnostic.org/eip155/caip19).
- Ethereum Improvement Proposals, [ERC-721](https://eips.ethereum.org/EIPS/eip-721).
- Ethereum Improvement Proposals, [EIP-1898](https://eips.ethereum.org/EIPS/eip-1898).
- Ethereum Improvement Proposals, [EIP-55](https://eips.ethereum.org/EIPS/eip-55).
