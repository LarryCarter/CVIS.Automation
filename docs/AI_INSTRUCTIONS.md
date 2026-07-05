## xUnit Trait Counting Rule

When generating xUnit `[Fact]` tests for this repository, do not put multiple category-counting `[Trait]` attributes on the same method.

If a test must count for multiple categories, generate one physical method per trait. Each method should have exactly one counting trait and a method name that includes the trait key.

## xUnit Category Trait Naming Rule

When generating duplicated xUnit test methods for countable traits:

- If the trait key is `Category`, use the trait value in the method name.
- If the trait key is not `Category`, use the trait value when meaningful, otherwise use the trait key.
- Never generate multiple methods named `*_Category_*` for different category values.

## xUnit Theory Trait Counting Rule

When generating xUnit `[Theory]` tests for this repository, do not put multiple category-counting `[Trait]` attributes on the same method.

If a theory must count for multiple categories, generate one physical theory method per trait. Preserve all data attributes (`[InlineData]`, `[MemberData]`, `[ClassData]`) on each duplicated theory method.

If the trait key is `Category`, use the trait value in the method name.
