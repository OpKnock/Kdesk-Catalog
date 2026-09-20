---
applyTo: "**/*.r **/*.rb **/*.sh"
---

# Api Test Data Factorybot

Builds test data factories with FactoryBot: trait definitions, sequences, associations, and on-the-fly attribute overrides for Rails APIs.

## Instructions

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
