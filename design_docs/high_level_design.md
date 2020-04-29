# High-level design

## Separation of logic from GitHub API calls

For the sake of testability, we keep logic separated from interaction
with the GitHub API, so that we can run most tests without going through
the API. This means that as much logic as possible is in classes that
are completely independent of the GitHub API. For querying, then, an
initial step is to fetch information from GitHub using as little logic
as possible, then storing this information in our own classes, with
which we can perform various logic.
