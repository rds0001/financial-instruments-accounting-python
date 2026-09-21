# Contributing

Contributions must preserve the public API contract, fail closed on incomplete
accounting inputs and include evidence for any change to a financial result.

1. Create a focused branch and explain the accounting or engineering reason.
2. Add an independent test for changed financial logic. Do not generate an
   expected value with the implementation under test.
3. Run the checks documented under `Local release verification` in
   `docs/operations.rst`.
4. Update the relevant API page, contract and correction record when behavior
   changes.

Never commit client data, credentials, licensed standard text or output labelled
as an official accounting conclusion. By contributing, you agree that your
contribution is licensed under Apache License 2.0.
