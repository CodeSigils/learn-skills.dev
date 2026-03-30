---
name: tdd
description: Guide Claude through test-driven development using the red-green-refactor cycle. Use this skill whenever the user wants to write code test-first, mentions TDD, asks to "write tests before the implementation", wants to do red-green-refactor, or asks you to implement a feature by starting with failing tests. Also trigger when the user says things like "let's do TDD", "drive this with tests", "test-first", or "make the tests pass". Even if they just say "add a feature" and the codebase already has a test suite, consider suggesting TDD if it fits naturally.
---

# TDD: Red-Green-Refactor

Test-driven development works in three tight repeating cycles:

1. **Red** — write a test that describes the behavior you want. Run it. It must fail (if it passes, either the behavior already exists or the test is wrong).
2. **Green** — write the *minimum* code needed to make that test pass. Resist the urge to generalize yet.
3. **Refactor** — clean up the code (and the test) without changing behavior. All tests must still pass when you're done.

Then repeat for the next behavior.

---

## How to work through a TDD session

### 0. Clarify scope before writing anything

Before touching code, make sure you understand:
- What behavior are we adding or fixing?
- Is there an existing test suite and runner? If so, identify the command to run tests (e.g., `pytest`, `npm test`, `go test ./...`, `cargo test`).
- What's the smallest slice of behavior worth starting with? (TDD shines when you slice features thin.)

Ask the user if anything is unclear. Don't assume.

### 1. Red — write a failing test

Write *one* test (or a small cohesive group) that expresses the desired behavior. Good TDD tests:
- Have descriptive names that read like sentences (`test_user_cannot_withdraw_more_than_balance`)
- Test behavior, not implementation details
- Are short and focused on a single concern

Run the tests and confirm the new test fails for the *right reason* — not a syntax error, import problem, or wrong assertion, but because the production code doesn't yet do the thing. Show the failure output to the user and briefly explain why the failure is expected.

**If the test passes immediately:** stop and investigate. Either the behavior already exists (tell the user) or the test isn't actually checking what you think it is (fix the test).

### 2. Green — make it pass, simply

Write the simplest production code that makes the failing test pass. "Simplest" means:
- No premature abstractions
- No handling of cases the tests don't cover yet
- Even a hardcoded return value is legitimate if it makes the test pass — the refactor step or the next test will force you to generalize

Run the full test suite. Show the output. All tests (old and new) should be green. If something that was passing is now failing, fix it before moving on.

### 3. Refactor — improve without changing behavior

Now that you have a safety net, improve the code:
- Remove duplication
- Clarify names and structure
- Apply relevant patterns or idioms
- Tidy up the tests too (they're code — they deserve care)

Run tests after every non-trivial change. Never move on with a failing test.

Refactoring is optional when the code is already clean. Don't refactor for its own sake.

### 4. Decide what's next

After a passing, clean cycle, pause and ask:
- Is there another behavior to add? (→ next red)
- Are there edge cases the current tests don't cover? (→ add more tests in the red step)
- Is the feature complete? (→ wrap up)

Show the user the full test output and invite them to steer.

---

## Communicating during the cycle

Keep the user oriented. At each phase, say which phase you're in and what you're about to do:

> "**Red:** I'm going to write a test for the case where a negative amount is deposited. Here's the test..."

> "**Green:** Tests are red. Writing the minimal code to handle this..."

> "**Refactor:** All green. I see some duplication between the two validation branches — let me clean that up."

Show test runner output at each phase (trimmed if it's noisy, but include the pass/fail summary and any failure messages).

---

## Handling tricky situations

**Legacy code with no tests:** Before adding new behavior, write a *characterization test* — a test that documents what the code currently does. This gives you a safety net before touching anything. Then apply TDD for the new behavior.

**Hard-to-test code:** If writing a test feels painful, that's usually a signal about design — the code may be doing too much, have hidden dependencies, or lack clear interfaces. Name the problem for the user and suggest a small design change (e.g., extracting a pure function) before writing the test.

**Mocking and faking:** Prefer testing through real interfaces when feasible. Use mocks or fakes when the real dependency is slow (network, DB), nondeterministic (random, time), or out of scope. When you do mock, mock at the boundary — not inside the unit under test.

**Test that's hard to make fail for the right reason:** Sometimes a test passes before you write any code because the logic already exists elsewhere. Tell the user, don't paper over it.

---

## Quality bar for tests

Good tests are:
- **Fast** — the suite should be runnable in seconds, not minutes
- **Isolated** — each test sets up its own state and doesn't depend on others
- **Readable** — another developer (or Claude in a future session) can understand the intent without digging into the implementation
- **Deterministic** — same inputs, same results, every time

If a test you write violates any of these, call it out and fix it.

---

## Example cycle (Python / pytest)

**Red:**
```python
def test_withdraw_raises_when_insufficient_funds():
    account = BankAccount(balance=10)
    with pytest.raises(InsufficientFundsError):
        account.withdraw(20)
```
Run: `pytest` → FAILED (InsufficientFundsError not defined, or withdraw doesn't raise)

**Green:**
```python
class InsufficientFundsError(Exception):
    pass

class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsError
        self.balance -= amount
```
Run: `pytest` → PASSED

**Refactor:**
- The error message could be more informative. Add it. Run tests. Still green.
- Nothing else needs changing here. Move on.

---

## Example with a real refactor (Python / pytest)

This shows what a refactor step looks like when it's genuinely motivated. A password validator gains rules one at a time — by the fourth rule, the repetition makes the right move obvious.

**Red → Green, cycle 1** (minimum length):
```python
def test_too_short_raises():
    with pytest.raises(ValueError, match="8 characters"):
        validate_password("abc")
```
```python
def validate_password(password):
    if len(password) < 8:
        raise ValueError("Password must contain at least 8 characters")
```
Run: FAILED → PASSED. Nothing to refactor yet.

**Red → Green, cycles 2–4** (uppercase, digit, special char — same pattern each time):
```python
def test_no_digit_raises():
    with pytest.raises(ValueError, match="digit"):
        validate_password("Abcdefgh!")
```
```python
    if not any(c.isdigit() for c in password):
        raise ValueError("Password must contain at least one digit")
```
After the fourth rule lands, the function is four nearly-identical `if`-blocks. That's the signal.

**Refactor:**

The duplication is structural — every check has the same shape: predicate + message. Extract a rule table:

```python
SPECIAL = set("!@#$%^&*")

_RULES = [
    (lambda p: len(p) >= 8,                     "Password must contain at least 8 characters"),
    (lambda p: any(c.isupper() for c in p),     "Password must contain at least one uppercase letter"),
    (lambda p: any(c.isdigit() for c in p),     "Password must contain at least one digit"),
    (lambda p: any(c in SPECIAL for c in p),    "Password must contain at least one special character"),
]

def validate_password(password):
    for passes, message in _RULES:
        if not passes(password):
            raise ValueError(message)
```
Run: `pytest` → still PASSED. Adding a fifth rule is now a one-liner in the table.
