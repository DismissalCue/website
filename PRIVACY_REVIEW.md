# Proposed privacy policy — October 25, 2026

Prepared at the owner's request for review. This branch does not change the live
GitHub Pages policy. Merging into `main` publishes the website automatically.

## What changed

- Replaced Driveline branding and the placeholder privacy address with
  DismissalCue / Dismissalcue LLC and the existing published privacy contact.
- Explained adult invitation-only accounts, school-controlled student records,
  separate per-child rights and school-controlled physical handoff.
- Distinguished foreground location for check-in from optional OS background
  geofences for local reminders. No automatic check-in or location-authorized
  release is promised.
- Described device-local biometrics and private keys without claiming the company
  collects Face ID templates.
- Removed claims of a universal legally required seven-year retention period,
  completed periodic independent audits, blanket TLS 1.3-only connections and
  guaranteed universal thirty-day school-data erasure.
- Added `data-requests.html`, with a discoverable email request path, verification
  steps, retained-school-record exceptions and a warning that requesting deletion
  is different from completion.
- Removed external font requests from these two privacy pages and disclosed the
  existing Google Fonts dependency on the home page. The site remains on GitHub
  Pages; this review does not change hosting or introduce analytics.

## Proposed business decisions

These are proposed operating limits, not assertions about universal legal
requirements. Approving the policy targets is distinct from confirming that
the software and support process implement them.

| Record | Proposed rule |
| --- | --- |
| Raw precise check-in coordinates | Maximum 7 days in primary storage and replicas |
| Student/permission/custody history | District-selected written schedule before live activation; documented preservation exceptions |
| Eligible adult account/profile information | Removal within 30 days after a verified request, with explained exceptions |
| Routine operational/security diagnostics | 30 days; separately documented incident or school records can have another schedule |
| Informational notifications and routine support correspondence | 90 days; school custody evidence follows the district's schedule |
| Staff-assistant conversation records | Maximum 30 days unless a specific longer need and period are documented |
| Backups | Rolling 35 days; deletion ledger replay before restored service resumes |

## Checks required before merging as an effective policy

1. Confirm the legal entity spelling and the privacy/support mailboxes. The
   addresses were already on the site; their inbound delivery and staffed
   request handling have not been verified in this review. Do not email
   verification secrets, identity-document photos or student rosters.
2. Confirm actual hosting/processing regions, current email/SMS providers and
   model-provider terms in the service-provider register and school agreement.
   The policy does not invent a hosting country or promise that every optional
   provider is currently enabled.
3. Implement and verify the in-app account-deletion initiation, identity review,
   account/session/provider revocation, safe active-pickup or staff-role handover,
   eligible data erasure, preservation notices and completion tracking. A mailto
   link is not evidence that this lifecycle exists or that store requirements
   are met.
4. Enforce the selected retention periods across primary data, replicas,
   notifications, support/assistant records and backup expiry. Prove restore
   deletion-ledger replay and district offboarding. Current read expiry or
   purging only when another write occurs is not proof of timely erasure.
5. Reconcile any existing customer commitments before replacing the old site's
   published retention promises. Do not silently reinterpret an existing
   agreement or remove a documented preservation requirement.
6. Obtain owner/legal review, set the effective date, remove the review banner
   and publish the final text only after commitments match actual operations.

This document is a technical/product review aid, not a certification of legal
compliance. The proposed pages are intentionally marked as drafts.

## Sources consulted

- [FTC: Protecting Personal Information](https://www.ftc.gov/business-guidance/resources/protecting-personal-information-guide-business): minimize retained data and document retention/disposal.
- [FTC: Privacy and Security](https://www.ftc.gov/business-guidance/privacy-security): make privacy promises match actual practices.
- [U.S. Department of Education: student privacy FAQs](https://studentprivacy.ed.gov/frequently-asked-questions): school control and permitted uses of education records.
- [Apple: account deletion](https://developer.apple.com/support/offering-account-deletion-in-your-app/).
- [Google Play: account deletion requirements](https://support.google.com/googleplay/android-developer/answer/13327111).


## October 25 owner authorization and technical review update

The owner authorized implementing gaps and publishing once practices support the
text; the support team owns requests, and no real school/family records beyond
synthetic demo data were reported. This approval does not itself prove an erasure
or retention control. Branding PR5 was merged separately. The proposed policy
remains a draft while the implementation work below is verified.

- Canonical pickup-loop branding is included; all public pages now use system
  fonts. The earlier homepage Google Fonts disclosure is superseded.
- Source review confirms check-in diagnostics store coarse coordinate-free
  bands. Do not describe raw coordinates as a retained database record without
  identifying an actual store. Foreground processing still needs disclosure.
- New app deletion initiation saves a self-only durable request, receipt and
  30-day review due date. Submission is **not** completed erasure. Support-side
  fulfillment, provider deletion and completion evidence remain required.
- New fixed-capability maintenance expires check-in diagnostics independently of
  new traffic, old encrypted browser attempts/sessions, and staff-assistant
  question/answer text. Other notification, support, tool/audit and school-record
  schedules are not proven by this worker.
- Rolling encrypted backup expiry and a separately retained deletion ledger with
  mandatory replay before restore remain unverified. Do not publish the proposed
  35-day promise yet.
- School-specific retention agreements, provider processing arrangements and
  the pre-live data activation gate still require evidence before live use.

This is an implementation status update, not a statement of legal certification
or App Store/Google Play privacy approval.

## October 26 implementation evidence

Main application commit 61e2ec12b3ae00753881a8cd6ca0a9c4ec86cc6d includes
in-app/web requests, separate support fulfillment and restore capabilities,
provider deletion verification, durable encrypted mirrored deletion evidence,
bounded diagnostics/assistant context and encrypted backup tooling. Full local
make check and make integration passed at schema76. Swift143 tests passed with
four external skips; Android tests/lint/build passed. CI/deployment is still
running; this branch remains a draft until hosted controls are verified.

Actual application and identity database backups were uploaded to private
DigitalOcean Spaces, downloaded, authenticated and restored into isolated
local disposable databases; those databases were removed. A baseline encrypted
deletion journal was mirrored separately. No actual account was deleted.

Retention copy now distinguishes transient raw coordinates from stored coarse
diagnostics, school notification records from manually reviewed support cases,
and transient assistant context from retained school audit facts. No universal
90-day notification purge is asserted. The reminder preference starts on but
requires separate OS permission. Support owns verified requests and must review
its queue and case retention. Provider lifecycle remains an additional pending
defense; do not say it is enabled merely because worker expiry is implemented.

Mailbox delivery and real-school agreements are not independently established by
these tests. No real customer school/family data was reported. The policy does
not certify FERPA/COPPA compliance, a completed independent audit or store approval.
