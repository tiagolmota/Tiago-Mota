# Graph Report - Tiago-Mota  (2026-05-27)

## Corpus Check
- 3423 files · ~2,090,543 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 155 nodes · 147 edges · 19 communities (13 shown, 6 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 4 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2d59202d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Security Vulnerabilities|Security Vulnerabilities]]
- [[_COMMUNITY_Angular Build Architecture|Angular Build Architecture]]
- [[_COMMUNITY_TypeScript Configuration|TypeScript Configuration]]
- [[_COMMUNITY_Dev Dependencies|Dev Dependencies]]
- [[_COMMUNITY_Angular Project Config|Angular Project Config]]
- [[_COMMUNITY_Angular Runtime Dependencies|Angular Runtime Dependencies]]
- [[_COMMUNITY_Build Output Options|Build Output Options]]
- [[_COMMUNITY_App Bootstrap & Config|App Bootstrap & Config]]
- [[_COMMUNITY_App Metadata|App Metadata]]
- [[_COMMUNITY_Course & Security Design|Course & Security Design]]
- [[_COMMUNITY_Project Documentation|Project Documentation]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]

## God Nodes (most connected - your core abstractions)
1. `AppComponent` - 17 edges
2. `compilerOptions` - 14 edges
3. `UFCD 10791 - Segurança Web com Java` - 6 edges
4. `app` - 6 edges
5. `development` - 6 edges
6. `Session Snapshot — 2026-05-27 09:51` - 5 edges
7. `Architecture Map — UFCD 10791` - 5 edges
8. `build` - 5 edges
9. `serve` - 5 edges
10. `token-optimizer` - 4 edges

## Surprising Connections (you probably didn't know these)
- `HTML Shell (index.html)` --references--> `AppComponent`  [EXTRACTED]
  index.html → src/app.component.ts
- `Application Bootstrap Entry (index.tsx)` --references--> `AppComponent`  [EXTRACTED]
  index.tsx → src/app.component.ts
- `AppComponent Template (app.component.html)` --shares_data_with--> `AppComponent`  [EXTRACTED]
  src/app.component.html → src/app.component.ts
- `Package Configuration (package.json)` --shares_data_with--> `Angular Project Configuration (angular.json)`  [INFERRED]
  package.json → angular.json
- `Security by Design` --rationale_for--> `UFCD 10791 - Web Application Development in Java`  [INFERRED]
  src/app.component.ts → metadata.json

## Hyperedges (group relationships)
- **Web Security Topics Covered in UFCD 10791** — concept_sql_injection, concept_xss, concept_csrf, concept_code_injection, concept_session_hijacking, concept_known_vulnerabilities, concept_brute_force, concept_security_by_design [EXTRACTED 1.00]
- **Angular Project Configuration Files** — angular_json_angularconfig, package_json_packageconfig, tsconfig_json_tsconfig, index_tsx_bootstrapentry [EXTRACTED 1.00]
- **Security Defense Patterns (Good Practices)** — concept_prepared_statements, concept_output_encoding, concept_csrf_tokens, concept_secure_cookies_https, concept_dependency_management, concept_rate_limiting [INFERRED 0.95]

## Communities (19 total, 6 thin omitted)

### Community 0 - "Security Vulnerabilities"
Cohesion: 0.11
Nodes (18): Brute Force Attacks and Account Lockout, Code Injection, Cross-Site Request Forgery (CSRF), Anti-CSRF Tokens, Active Dependency Management (OWASP Dependency-Check), IntersectionObserver for Scroll Animations, Using Components with Known Vulnerabilities, Output Encoding and Input Validation (XSS Defense) (+10 more)

### Community 1 - "Angular Build Architecture"
Cohesion: 0.12
Nodes (19): architect, build, serve, builder, configurations, defaultConfiguration, development, production (+11 more)

### Community 2 - "TypeScript Configuration"
Cohesion: 0.11
Nodes (18): angularCompilerOptions, disableTypeScriptVersionCheck, compilerOptions, allowJs, experimentalDecorators, isolatedModules, jsx, lib (+10 more)

### Community 3 - "Dev Dependencies"
Cohesion: 0.09
Nodes (22): dependencies, @angular/build, @angular/cli, @angular/common, @angular/compiler, @angular/compiler-cli, @angular/core, @angular/platform-browser (+14 more)

### Community 4 - "Angular Project Config"
Cohesion: 0.20
Nodes (9): prefix, projectType, root, sourceRoot, newProjectRoot, projects, app, $schema (+1 more)

### Community 5 - "Angular Runtime Dependencies"
Cohesion: 0.29
Nodes (6): Files Changed, Last Turn, Otimização total estimada: ~88-95% menos tokens por sessão, Recent Commits, Session Snapshot — 2026-05-27 09:51, Token Estimate

### Community 6 - "Build Output Options"
Cohesion: 0.33
Nodes (6): options, browser, outputPath, tsConfig, base, browser

### Community 7 - "App Bootstrap & Config"
Cohesion: 0.50
Nodes (5): Angular Project Configuration (angular.json), Zoneless Change Detection (Angular 21), Application Bootstrap Entry (index.tsx), Package Configuration (package.json), TypeScript Configuration (tsconfig.json)

### Community 8 - "App Metadata"
Cohesion: 0.50
Nodes (3): description, name, requestFramePermissions

### Community 9 - "Course & Security Design"
Cohesion: 0.67
Nodes (3): Security by Design, UFCD 10791 - Web Application Development in Java, App Metadata (metadata.json)

### Community 11 - "Community 11"
Cohesion: 0.20
Nodes (9): hooks, PreToolUse, Stop, UserPromptSubmit, mcpServers, token-optimizer, args, command (+1 more)

### Community 12 - "Community 12"
Cohesion: 0.25
Nodes (7): Architecture Map — UFCD 10791, code:block1 (Tiago-Mota/), code:block2 (index.html (importmap CDN)), Data Flow, File Tree, Key Patterns, Security Topics (IDs)

### Community 13 - "Community 13"
Cohesion: 0.29
Nodes (6): Docs (load when needed), graphify, Key Rules, Never Auto-Load, Session Start ⚡ (~800 tokens), UFCD 10791 - Segurança Web com Java

## Knowledge Gaps
- **88 isolated node(s):** `Files Changed`, `Recent Commits`, `Token Estimate`, `Otimização total estimada: ~88-95% menos tokens por sessão`, `code:block1 (Tiago-Mota/)` (+83 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AppComponent` connect `Security Vulnerabilities` to `App Bootstrap & Config`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Why does `architect` connect `Angular Build Architecture` to `Angular Project Config`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Why does `build` connect `Angular Build Architecture` to `Build Output Options`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **What connects `Files Changed`, `Recent Commits`, `Token Estimate` to the rest of the system?**
  _97 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Security Vulnerabilities` be split into smaller, more focused modules?**
  _Cohesion score 0.1067193675889328 - nodes in this community are weakly interconnected._
- **Should `Angular Build Architecture` be split into smaller, more focused modules?**
  _Cohesion score 0.11695906432748537 - nodes in this community are weakly interconnected._
- **Should `TypeScript Configuration` be split into smaller, more focused modules?**
  _Cohesion score 0.10526315789473684 - nodes in this community are weakly interconnected._