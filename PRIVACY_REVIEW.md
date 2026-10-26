# Privacy publication record — October 26, 2026

The owner authorized fixing gaps and publishing the policy. The support team
owns privacy/deletion requests; the owner reports no real school/family records
beyond the synthetic demo. This record distinguishes technical evidence from
legal certification, store approval and live-school activation.

## Published scope

The policy explains school-controlled student records, adult accounts, separate
per-child rights, foreground check-in location, optional half-mile reminders,
local biometrics, service recipients, retention, deletion and retained-record
exceptions. The reminder preference starts on but cannot activate background
location or notifications without the adult's OS permission.

Raw precise coordinates are processed during check-in; diagnostics retain
coordinate-free bands. School notification/delivery/audit facts follow the
school's written schedule, rather than an invented universal 90-day purge. Support
case correspondence is manually reviewed for removal 90 days after closure.

## Verified technical evidence

Application commit 61e2ec12b3ae00753881a8cd6ca0a9c4ec86cc6d passed full local
make check and make integration at schema 76. CI 40329515692 passed all checks,
vulnerability gates, signed-artifact verification and hosted deployment. The
server's deployed marker and schema 76 were independently verified.

- In-app and web self-only deletion requests have durable references. A request
  receipt does not mean completed erasure.
- Root-only support fulfillment revokes access, verifies identity-provider
  deletion, removes eligible adult profile data and mirrors encrypted deletion
  evidence. Active pickup, offline reconciliation or staff handover can block
  unsafe fulfillment. Tests preserve school custody and original request dates.
- A separate isolated restore capability replays deletion evidence and re-expires
  transient data before cutover. Tests cover missing, tampered and truncated
  evidence. No actual demo account was erased during this work.
- The hosted privacy-maintenance service is active and independently expires
  diagnostics and assistant prompt/answer/tool context without new traffic.
  Six/29-day cutoffs leave margin before the public seven/30-day active limits.
- The private NYC3 backup bucket has bucket-limited worker credentials. Both
  actual encrypted databases were downloaded, authenticated and restored into
  disposable isolated local databases; the test databases were removed.
- The deployed backup service completed successfully October 26 at 13:47 UTC,
  uploading application and identity backups. Its daily timer is active and
  worker expiry is bounded below the 35-day maximum. Independent provider
  lifecycle configuration is not claimed to be enabled.
- The encrypted deletion journal was independently mirrored. Its keys and
  checkpoint are outside database backups and private credentials stay out of
  Git and public pages.
- The log-retention service completed successfully; its timer is active and all
  five hosted dependency containers use journald rather than indefinite Docker
  JSON logs. Routine logs have bounded retention; preserved incident evidence
  needs its own documented owner, purpose and expiry.
- The public deletion page route returns HTTP 200. Privacy/request layouts fit
  390px mobile and 1280px desktop, with resolving local links.

## Operational and launch limits

Support must monitor both published inboxes, review requests daily, verify
identity through a trusted process, explain delays/retained categories and record
completion. Inbound mailbox delivery was not independently tested by this task;
no unrequested test messages were sent. Manual procedures are not described as
automated mailbox deletion.

Before live-school activation, complete the school-specific retention/processing
agreements, provider register, full device/GPS/offline/reconciliation rehearsals,
independent security review and remaining product release gates. The policy does
not certify FERPA/COPPA compliance, claim an uncompleted audit, or establish App
Store/Google Play acceptance. Native builds are still prepublication artifacts.

## Primary guidance checked

- https://www.ftc.gov/business-guidance/resources/protecting-personal-information-guide-business
- https://studentprivacy.ed.gov/frequently-asked-questions
- https://developer.apple.com/help/app-review/guideline-reference/5-1-1-account-deletion
- https://support.google.com/googleplay/android-developer/answer/13327111
- https://developer.apple.com/app-store/app-privacy-details/
- https://support.google.com/googleplay/android-developer/answer/10787469
