---
name: "laravel"
description: "Builds PHP web applications with Laravel: artisan commands, migrations, queues, scheduling, and testing. Use when working with laravel artisan, laravel queues, backend or when the user mentions laravel artisan, laravel queues, backend."
globs: ["**/*.php", "**/*.r", "**/*.sh"]
alwaysApply: false
---

Builds PHP web applications with Laravel: artisan commands, migrations, queues, scheduling, and testing.

## Agentic Workflow: Read -> Reason -> Act (laravel)

You are **laravel** (backend/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `laravel`
- Domain: Builds PHP web applications with Laravel: artisan commands, migrations, queues, scheduling, and testing.
- **laravel-artisan**: Scaffold and manage Laravel applications. — `composer create-project laravel/laravel myapp`
- **laravel-queues**: Run queue workers and the scheduler. — `php artisan queue:work`
- Check `knowledge` and `prerequisites: composer, php`

### 2. Reason — think for `laravel`
- For `laravel-artisan`: Scaffold and manage Laravel applications. — decide which checks to run
- For `laravel-queues`: Run queue workers and the scheduler. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `laravel` tools
- Tools: `Glob`, `Grep`, `Read`, `Composer`, `Php` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `laravel:b17a9c39`

# Laravel

PHP web framework with batteries included.

## When to Use

- Full-stack PHP apps with Eloquent ORM
- REST APIs with built-in auth and validation
- Apps needing queues, caching, and scheduling out of the box

## Commands

```bash
# Create app
composer create-project laravel/laravel myapp

# Dev server
php artisan serve

# Scaffolding
php artisan make:model Order -m
php artisan make:controller OrderController --resource

# Database
php artisan migrate
php artisan migrate:fresh --seed

# Shell
php artisan tinker

# Routes
php artisan route:list

# Queues
php artisan queue:work
php artisan queue:listen --tries=3
php artisan queue:retry all

# Scheduler
php artisan schedule:work
php artisan schedule:list
```

## Job Example

```php
// app/Jobs/SendEmail.php
class SendEmail implements ShouldQueue
{
    public function handle(): void
    {
        Mail::to($this->user)->send(new WelcomeMail());
    }
}
```

## Best Practices

- Run migrations via deploy pipelines, never ad-hoc in prod
- Keep controllers thin; push logic into services and jobs
- Use queue:work under supervisor in production
- Schedule tasks in the kernel and run schedule:run via cron once
- Cache config/routes in prod: php artisan config:cache

## Capabilities

### laravel-artisan
Scaffold and manage Laravel applications.

**Parameters:**
- `name` (string): Artisan make target name
- `flags` (string): Artisan flags like -m --resource

**Commands:**
- `composer create-project laravel/laravel myapp`
- `php artisan serve`
- `php artisan make:model Order -m`
- `php artisan migrate`
- `php artisan tinker`

**Examples:**
- php artisan make:controller OrderController --resource
- php artisan migrate:fresh --seed
- php artisan route:list --path=api

### laravel-queues
Run queue workers and the scheduler.

**Parameters:**
- `connection` (string): Queue driver: redis, database
- `tries` (integer): Max attempts

**Commands:**
- `php artisan queue:work`
- `php artisan queue:listen --tries=3`
- `php artisan schedule:work`
- `php artisan queue:table`
- `php artisan schedule:list`

**Examples:**
- php artisan queue:work redis --timeout=60
- php artisan schedule:test
- php artisan queue:retry all

## References
- [Laravel Docs](https://laravel.com/docs)
- [Laravel Queues](https://laravel.com/docs/queues)