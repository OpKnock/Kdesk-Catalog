# Bugsnag Error Tracking

Tracks errors with Bugsnag: uploading source maps, notifying via API, and managing releases with the bugsnag CLI.

## Instructions

# Bugsnag Error Tracking

## What this skill does

Tracks errors with Bugsnag: uploading source maps per release so stack traces are readable, sending test notifications to the notify API, and recording releases via the bugsnag CLI.

## When to use

- Minified JS stack traces are unreadable (missing source maps)
- Verifying API keys/notifications from CI
- Associating errors with app versions

## Real commands

```bash
# Upload a source map
bugsnag-cli sourcemap upload --api-key $BUGSNAG_API_KEY --app-version 1.2.3 --source-map ./dist/app.js.map

# Alternative: npx sourcemap uploader
npx bugsnag-sourcemaps upload --api-key $KEY --minified-file dist/bundle.js --source-map dist/bundle.js.map --app-version 1.2.3

# Send a test event
curl -X POST https://notify.bugsnag.com/ -H "Content-Type: application/json" -d '{"apiKey":"$KEY","events":[{"payloadVersion":4,"exceptions":[{"errorClass":"Test","message":"hello"}]}]}'

# Record a release
bugsnag-cli release --api-key $KEY --app-version 1.2.3 --stage production
```

## Testing

- Send a notify probe and confirm 200
- Upload a map then trigger an error; verify the stack trace is de-minified

## Best practices

- Upload source maps in the same CI job as the deploy
- Pin the app-version to your release tag
- Send releases with stage + metadata for filtering

## Capabilities

### sourcemaps
Upload source maps so stack traces are readable.

**Commands:**
- `bugsnag-cli sourcemap upload --api-key $BUGSNAG_API_KEY --app-version 1.2.3 --source-map ./dist/app.js.map`
- `npx bugsnag-sourcemaps upload --api-key $BUGSNAG_API_KEY --minified-file dist/bundle.js --source-map dist/bundle.js.map --app-version 1.2.3`
- `bugsnag-cli sourcemap upload --api-key $KEY --app-version 1.2.3 --source-map ./dist/*.map`
- `npx bugsnag-sourcemaps upload --api-key $KEY --minified-file dist/bundle.js --source-map dist/bundle.js.map --public-path /assets`

**Examples:**
- bugsnag-cli sourcemap upload --api-key $BUGSNAG_API_KEY --app-version 1.2.3 --source-map ./dist/app.js.map
- npx bugsnag-sourcemaps upload --api-key $KEY --minified-file dist/bundle.js --source-map dist/bundle.js.map --app-version 1.2.3
- npx bugsnag-sourcemaps upload --api-key $KEY --minified-file dist/app.js --source-map dist/app.js.map --upload-sources

### notify-api
Send errors to Bugsnag's notify API.

**Commands:**
- `curl -X POST https://notify.bugsnag.com/ -H "Content-Type: application/json" -d '{"apiKey":"$BUGSNAG_API_KEY","events":[{"payloadVersion":4,"exceptions":[{"errorClass":"TestError","message":"manual notify"}],"severity":"warning"}]}'`
- `curl -s -o /dev/null -w "%{http_code}\n" -X POST https://notify.bugsnag.com/ -H "Content-Type: application/json" -d '{"apiKey":"$BUGSNAG_API_KEY","events":[{"payloadVersion":4,"exceptions":[{"errorClass":"Probe","message":"healthcheck"}]}]}'`
- `curl -s -X POST https://notify.bugsnag.com/ -H "Content-Type: application/json" -d '{"apiKey":"$BUGSNAG_API_KEY","events":[{"payloadVersion":4,"exceptions":[{"errorClass":"Probe","message":"ok"}],"severity":"info"}]}'`

**Examples:**
- curl -X POST https://notify.bugsnag.com/ -H "Content-Type: application/json" -d '{"apiKey":"$KEY","events":[{"payloadVersion":4,"exceptions":[{"errorClass":"Test","message":"hello"}]}]}'
- curl -s -o /dev/null -w "%{http_code}\n" -X POST https://notify.bugsnag.com/ -H "Content-Type: application/json" -d '{"apiKey":"$KEY","events":[{"payloadVersion":4,"exceptions":[{"errorClass":"Probe","message":"test"}]}]}'
- curl -s -X POST https://notify.bugsnag.com/ -H "Content-Type: application/json" -d '{"apiKey":"$KEY","events":[{"payloadVersion":4,"exceptions":[{"errorClass":"InfoProbe","message":"ok"}],"severity":"info","context":"ci"}]}'

### releases
Track releases so Bugsnag links errors to versions.

**Commands:**
- `bugsnag-cli release --api-key $BUGSNAG_API_KEY --app-version 1.2.3 --stage production`
- `bugsnag-cli releases list --api-key $KEY --project-root .`
- `bugsnag-cli --version`
- `bugsnag-cli help`

**Examples:**
- bugsnag-cli release --api-key $KEY --app-version 1.2.3 --stage production
- bugsnag-cli release --api-key $KEY --app-version 1.2.4 --stage staging --metadata "commit=$(git rev-parse HEAD)"
- bugsnag-cli releases list --api-key $KEY
