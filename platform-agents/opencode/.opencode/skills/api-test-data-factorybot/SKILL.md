---
name: "api-test-data-factorybot"
description: "Builds test data factories with FactoryBot: trait definitions, sequences, associations, and on-the-fly attribute overrides for Rails APIs. Use when working with factorybot, factory testing or when the user mentions factorybot, factory testing."
---

Builds test data factories with FactoryBot: trait definitions, sequences, associations, and on-the-fly attribute overrides for Rails APIs.

## Agentic Workflow: Read -> Reason -> Act (api-test-data-factorybot)

You are **Api Test Data Factorybot** (testing) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — testing context for `api-test-data-factorybot`
- Domain: Builds test data factories with FactoryBot: trait definitions, sequences, associations, and on-the-fly attribute overrides for Rails APIs.
- **factorybot**: Define and use model factories — `bundle add factory_bot_rails`
- **factory-testing**: Lint and verify factories — `bundle exec rails runner "FactoryBot.lint"`
- Check `knowledge` and `prerequisites: faker, node.js, python`

### 2. Reason — think for `api-test-data-factorybot`
- For `factorybot`: Define and use model factories — decide which checks to run
- For `factory-testing`: Lint and verify factories — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-test-data-factorybot` tools
- Tools: `Glob`, `Grep`, `Read`, `Bundle` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-test-data-factorybot:72d25b91`

# API Test Data v3 - Factories

Test data factories with FactoryBot.

## What This Skill Does
- Defines reusable model factories
- Composes fixtures with traits
- Seeds large datasets for tests

## When to Use
- Rails API test suites
- Replacing brittle hardcoded fixtures
- Building association graphs

## Real Commands

```bash
bundle add factory_bot_rails
bundle exec rails runner "FactoryBot.create_list(:user, 50)"
bundle exec rails runner "FactoryBot.lint"
```

## Factory Example

```ruby
factory :user do
  sequence(:email) { |n| "user#{n}@example.com" }
  name { Faker::Name.name }
  role { :member }

  trait :admin do
    role { :admin }
  end
end
```

## Testing
- Run FactoryBot.lint to validate factories
- Test every trait with a build call
- Verify associations resolve


## Best Practices
- Use sequences for uniqueness
- Override attributes explicitly in tests
- Avoid factory hierarchies deeper than needed

## Capabilities

### factorybot
Define and use model factories

**Parameters:**
- `factory` (string): Factory name
- `trait` (string): Trait to apply
- `attributes` (object): Attribute overrides

**Commands:**
- `bundle add factory_bot_rails`
- `bundle exec rails generate model User name:string email:string role:string`
- `bundle exec rails runner "puts FactoryBot.create(:user).id"`
- `bundle exec rails runner "FactoryBot.create_list(:user, 50)"`
- `bundle exec rails runner "puts FactoryBot.create(:user, :admin, name: 'root').role"`

**Examples:**
- FactoryBot.create(:user) builds and saves a record
- create_list(:user, 50) seeds bulk data
- traits like :admin plus overrides compose fixtures

### factory-testing
Lint and verify factories

**Commands:**
- `bundle exec rails runner "FactoryBot.lint"`
- `bundle exec rspec spec/factories_spec.rb`
- `bundle exec rails db:seed`
- `bundle exec rails runner "puts FactoryBot.build(:user).email"`

**Examples:**
- -cli --help
- -api --help

## References
- [FactoryBot Docs](https://github.com/thoughtbot/factory_bot/blob/main/GETTING_STARTED.md)
- [FactoryBot Rails](https://github.com/thoughtbot/factory_bot_rails)
