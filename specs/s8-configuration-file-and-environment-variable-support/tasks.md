# S8.6 — Configuration File and Environment Variable Support: Tasks

## Implementation Tasks
- [ ] Create `ops/config_loader.py` with `ConfigLoader`
- [ ] Implement YAML file loading
- [ ] Implement environment variable override with `TIMETRAVEL_` prefix
- [ ] Implement precedence chain (env > file > defaults)
- [ ] Implement startup validation

## Testing Tasks
- [ ] Test loading from config file
- [ ] Test environment variable override
- [ ] Test precedence (env overrides file overrides default)
- [ ] Test invalid config value produces startup error
- [ ] Test missing config file handled gracefully
