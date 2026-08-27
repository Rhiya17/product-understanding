# Tripo3D / fal.ai commercial-license review

**Review date:** 2026-08-27

**Sources retrieved:** 2026-08-27

**Artifact reviewed:** `tripo-probe-01`, request `01a0410a-752c-7570-aa0f-a0eb20316afb`, submitted to the paid fal endpoint `tripo3d/h3.1/multiview-to-3d` on 2026-08-27.

**Status:** RESEARCH COMPLETE; OWNER DECISION OPEN

**Owner decision:** `null`

**Approved by:** `null`

**Distribution pending decision:** **INTERNAL ONLY — DO NOT SHIP**

This is an operational rights review, not legal advice. It records the current official language and a conservative recommendation; the owner makes the shipping decision.

## Short answer

1. **Commercial use:** conditionally yes for a paying API customer. fal marks the exact H3.1 multiview endpoint **“Commercial use”**, and Tripo's paid-user terms grant broad rights to use, modify, create derivatives, distribute, license, display, and derive revenue from outputs. The condition is that the fal partner invocation carries the advertised commercial entitlement and that the customer owns or has permission for the source photographs and depicted product IP.
2. **Attribution, resale, ownership:** no express attribution requirement was found in the reviewed Tripo terms, fal terms, API supplement, endpoint page, or Tripo pricing page. Tripo's paid-user clause grants broad output rights but also requires a royalty-free, perpetual, non-exclusive service-use/display authorization to Tripo. fal's current terms do not expressly assign Output Content ownership to the customer; they instead preserve customer ownership of inputs, disclaim output originality/non-infringement, and make third-party-model terms applicable. Resale of fal service rights is barred; Tripo's paid-output rights include transfer and licensing, but neither provider authorizes reselling access to the generator or using outputs to build a competing model/service.
3. **Serving derived renders:** no reviewed term expressly prohibits serving static or animated renders derived from a commercially entitled output. Tripo's paid-user display, derivative-work, distribution, and revenue rights support that use. Do not expose the Tripo/fal API, sell service access, train a competing model from the output, or assume the provider clears Graco trademarks, trade dress, copyrights, or the input photographs.

## Official-source findings

### Tripo3D

The [Tripo Terms of User Agreement](https://www.tripo3d.ai/terms), last updated July 11, 2025, distinguish free from paid users:

- Section 5.2.1 says, **“Tripo retains all rights”** in free-user inputs and outputs. The [current pricing page](https://www.tripo3d.ai/pricing) likewise describes the Free plan as **“Public Models · Non-Commercial Use.”**
- Section 5.2.2 says paid users **“generally have all rights”** and then enumerates use, modification, derivative works, distribution, transfer, licensing, public display, and revenue generation. The same clause grants Tripo a royalty-free, perpetual, irrevocable, worldwide, non-exclusive authorization to use/display inputs and outputs as needed to provide the service.
- Section 3.2 permits lawful commercial/non-commercial output use but prohibits using outputs to create competing models/services and prohibits making the Generative 3D Foundation Model Service available to third parties without written consent.
- The terms place third-party-rights responsibility on the user and disclaim non-infringement and output reliability. They do not promise exclusivity.
- The reviewed terms contain no express attribution requirement. Absence of a clause is not a provider warranty, so the saved terms version and paid entitlement should travel with the asset record.

The Studio pricing page is supporting context, not the fal API contract: Pro, Max, and Team list “Private Models · Commercial Use,” while Free is non-commercial. It confirms Tripo's plan-level distinction but does not by itself prove which direct-Studio tier maps to a fal partner request.

### fal.ai and the Tripo partner endpoint

The [exact fal endpoint page](https://fal.ai/models/tripo3d/h3.1/multiview-to-3d/api) identifies `tripo3d/h3.1/multiview-to-3d` as a **“Commercial use”** partner model and documents the generated GLB/PBR model as Output.

The [fal Terms of Service](https://fal.ai/legal/terms-of-service), last updated July 31, 2026, and the [API Services Supplemental Terms](https://fal.ai/legal/api-services) add these constraints:

- A paid API customer may integrate the service in a Customer Solution and allow end users to use it during the term, but must not expose the API directly.
- fal says Output Content may not be unique and provides no originality or non-infringement warranty. The API supplement says fal does not warrant that Output Content **“will not infringe rights of any third party.”**
- Customer ownership is stated for Customer Input, not expressly for Output Content. fal retains the service/platform IP; the agreement does not state that fal owns the generated output either.
- Partner models are Third-Party Materials and may carry additional provider terms. Outputs from them cannot be used to build or improve a competing model/service, reproduce training data, or closely mimic training assets.
- Customer service/API rights cannot be resold, transferred, assigned, or sublicensed. This is distinct from distributing a rendered output under the applicable output rights.

## Answers for this asset

| Question | Finding | Confidence / condition |
|---|---|---|
| May the paying API customer use the generated mesh commercially? | **Yes, conditionally.** The exact fal listing says commercial use, and Tripo paid-user terms enumerate commercial exploitation rights. | Moderate-high. Preserve proof that this request was a paid fal partner request; obtain written fal/Tripo confirmation if the owner needs an unqualified chain-of-title statement. |
| May renders/derivatives be served commercially? | **Yes, conditionally.** Derivative-work, display, distribution, and revenue rights cover renders; no render-serving prohibition was found. | Moderate-high, subject to input/product IP clearance and the partner-chain condition. |
| Is attribution required? | **No express provider attribution requirement found.** | Moderate. Recheck the preserved terms if the asset is shipped later. Product/trademark notices are a separate decision. |
| May the raw output be resold or licensed? | Tripo paid-user language includes transfer and licensing, but fal does not expressly assign output ownership. | Moderate-low for raw-asset resale; obtain written confirmation before selling the GLB/texture as an asset. Derived-render distribution is the narrower, better-supported use. |
| May the API/service be resold or exposed? | **No.** fal bars resale/transfer of service rights and direct API exposure; Tripo bars making its foundation-model service available without consent. | High. |
| Does either provider clear third-party product IP? | **No.** Both put lawful-input/non-infringement responsibility on the customer and disclaim output non-infringement. | High. |

## Recommended owner disposition

Record **CONDITIONAL COMMERCIAL APPROVAL FOR DERIVED RENDERS ONLY** if—and only if—the owner confirms all of the following in the asset record:

1. the fal invoice/account record for request `01a0410a-752c-7570-aa0f-a0eb20316afb` establishes paid access to the endpoint carrying fal's “Commercial use” label;
2. the organization is authorized to use the two source product photographs and to depict the Graco Ready2Jet product, marks, and trade dress in the intended serving context;
3. serving is limited to derived rendered media, not resale of the raw Tripo GLB/texture or access to fal/Tripo services;
4. the output is not used to train, fine-tune, or build a competing 3D model/service; and
5. this review, the generation date, request record, invoice/entitlement evidence, and the retrieved terms versions are retained together.

If any condition is not documented, keep the current **INTERNAL ONLY** disposition and request written commercial-rights confirmation from fal that expressly covers Tripo partner outputs and derived renders. This recommendation does not approve the asset; `approved_by` remains `null` until the owner records a decision.
