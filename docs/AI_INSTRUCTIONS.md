## xUnit Trait Counting Rule

When generating xUnit `[Fact]` tests for this repository, do not put multiple category-counting `[Trait]` attributes on the same method.

If a test must count for multiple categories, generate one physical method per trait. Each method should have exactly one counting trait and a method name that includes the trait key.
