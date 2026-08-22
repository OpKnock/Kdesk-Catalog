---
name: "form-validation-engineer"
description: "Implements client and server-side form validation with Zod, React Hook Form, and HTML constraint validation, with linting gates in CI."
type: knowledge
triggers: ["form-validation-engineer", "zod-schemas", "html-validation"]
---

# form-validation-engineer

Implements client and server-side form validation with Zod, React Hook Form, and HTML constraint validation, with linting gates in CI.

## Instructions

# Form Validation

Validate user input at every layer: client UX, server contract, and persistence.

## When to Use

- Building signup, checkout, or settings forms
- Reusing validation rules between client and server
- Enforcing field requirements and formatting consistently

## Single source of truth with Zod

```typescript
import { z } from 'zod';

export const signupSchema = z.object({
  email: z.string().trim().email().max(254),
  password: z.string().min(12).regex(/[^A-Za-z0-9]/),
  age: z.coerce.number().int().min(13).max(130).optional(),
  terms: z.literal(true, { errorMap: () => ({ message: 'Terms must be accepted' }) })
});

export type SignupInput = z.infer<typeof signupSchema>;
```

## Wire into React Hook Form

```typescript
const { register, handleSubmit, formState: { errors } } = useForm<SignupInput>({
  resolver: zodResolver(signupSchema),
  mode: 'onBlur'
});
```

Validate on blur (not every keystroke) to reduce noise, and show errors under fields with `aria-invalid`.

## Server-side revalidation

Never trust the client: re-run the same schema in the API route/action and return 422 with field errors.

## HTML constraint attributes

Even with a JS framework, keep native attributes:

```html
<input type="email" required minlength="3" maxlength="254" autocomplete="email" aria-describedby="email-hint" />
```

## Lint gates

```bash
npx html-validate --rule 'input-missing-type:error' --max-warnings 5 src/
```

## Best practices

- Trim and normalize before validating (email lowercase, phone digits).
- Limit length on every string field to prevent abuse.
- Test both valid and invalid fixtures in unit tests.
- Keep error messages specific and user-localizable.

## Capabilities

### zod-schemas
Define and test typed validation schemas with Zod.

**Commands:**
- `npm init -y && npm install zod react-hook-form @hookform/resolvers`
- `node -e "const {z}=require('zod'); const s=z.object({email:z.string().email(),age:z.coerce.number().min(18)}); console.log(s.safeParse({email:'a@b.co',age:'25'}))"`
- `npx tsx validate-form.ts`
- `npm run build`
- `npm test`

**Examples:**
- node --eval "const {z}=require('zod');z.string().email().safeParse('bad')"
- npx tsx -e "import {z} from 'zod'; const s=z.object({name:z.string().min(2).max(60)}); console.log(s.safeParse({name:''}))"
- npm test -- --runInBand

### html-validation
Lint HTML forms for accessibility and constraint validation issues.

**Commands:**
- `npx html-validate index.html`
- `npx html-validate --rule 'form-dup-name:error' src/**/*.html`
- `npx html-validate --formatter json index.html`
- `npx html-validate --config .htmlvalidate.json app/`
- `npx html-validate --max-warnings 5 src/`

**Examples:**
- npx html-validate --rule 'input-missing-type:error' form.html
- npx html-validate --formatter stylish index.html
- npx html-validate --config .htmlvalidate.json src --max-warnings 10
