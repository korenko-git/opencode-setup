# Dependency Vulnerability Scanning & Audit

Expert in dependency security: CVE vulnerability scanning, SBOM generation, supply chain security,
license compliance, and automated remediation across all major package ecosystems.

---

## 1. Multi-Ecosystem Scanner

```python
import subprocess, json, requests
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Vulnerability:
    package: str
    version: str
    vulnerability_id: str
    severity: str
    cve: List[str]
    cvss_score: float
    fixed_versions: List[str]
    source: str

class DependencyScanner:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)

    def detect_ecosystems(self) -> List[str]:
        ecosystem_files = {
            'npm':   ['package.json', 'package-lock.json'],
            'pip':   ['requirements.txt', 'pyproject.toml', 'Pipfile'],
            'go':    ['go.mod'],
            'cargo': ['Cargo.toml'],
            'ruby':  ['Gemfile'],
            'java':  ['pom.xml', 'build.gradle'],
            'php':   ['composer.json'],
        }
        return [eco for eco, patterns in ecosystem_files.items()
                if any(list(self.project_path.glob(f"**/{p}")) for p in patterns)]

    def scan_all(self) -> Dict[str, Any]:
        results = {
            'timestamp': datetime.now().isoformat(),
            'ecosystems': {},
            'vulnerabilities': [],
            'summary': {'total': 0, 'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        }
        scanners = {
            'npm': self.scan_npm, 'pip': self.scan_python,
            'go': self.scan_go, 'cargo': self.scan_rust
        }
        for eco in self.detect_ecosystems():
            if eco in scanners:
                eco_results = scanners[eco]()
                results['ecosystems'][eco] = eco_results
                results['vulnerabilities'].extend(eco_results.get('vulnerabilities', []))

        self._update_summary(results)
        results['remediation_plan'] = self.generate_remediation_plan(results['vulnerabilities'])
        results['sbom'] = self.generate_sbom(results['ecosystems'])
        return results

    def scan_npm(self) -> Dict:
        try:
            result = subprocess.run(['npm', 'audit', '--json'],
                cwd=self.project_path, capture_output=True, text=True, timeout=120)
            audit = json.loads(result.stdout)
            vulns = []
            for vid, v in audit.get('vulnerabilities', {}).items():
                vulns.append({
                    'package': v.get('name', vid), 'version': v.get('range', ''),
                    'vulnerability_id': vid, 'severity': v.get('severity', 'UNKNOWN').upper(),
                    'cve': v.get('cves', []), 'fixed_in': v.get('fixAvailable', {}).get('version', 'N/A'),
                    'source': 'npm_audit'
                })
            return {'ecosystem': 'npm', 'vulnerabilities': vulns}
        except Exception as e:
            return {'ecosystem': 'npm', 'vulnerabilities': [], 'error': str(e)}

    def scan_python(self) -> Dict:
        try:
            result = subprocess.run(['safety', 'check', '--json'],
                cwd=self.project_path, capture_output=True, text=True, timeout=120)
            data = json.loads(result.stdout)
            vulns = [{'package': v.get('package_name'), 'version': v.get('analyzed_version'),
                      'vulnerability_id': v.get('vulnerability_id'), 'severity': 'HIGH',
                      'fixed_in': v.get('fixed_version'), 'source': 'safety'} for v in data]
            return {'ecosystem': 'python', 'vulnerabilities': vulns}
        except Exception as e:
            return {'ecosystem': 'python', 'vulnerabilities': [], 'error': str(e)}

    def scan_go(self) -> Dict:
        try:
            result = subprocess.run(['govulncheck', '-json', './...'],
                cwd=self.project_path, capture_output=True, text=True, timeout=180)
            vulns = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    d = json.loads(line)
                    if d.get('finding'):
                        f = d['finding']
                        vulns.append({'package': f.get('osv'), 'vulnerability_id': f.get('osv'),
                                      'severity': 'HIGH', 'source': 'govulncheck'})
            return {'ecosystem': 'go', 'vulnerabilities': vulns}
        except Exception as e:
            return {'ecosystem': 'go', 'vulnerabilities': [], 'error': str(e)}

    def scan_rust(self) -> Dict:
        try:
            result = subprocess.run(['cargo', 'audit', '--json'],
                cwd=self.project_path, capture_output=True, text=True, timeout=120)
            data = json.loads(result.stdout)
            vulns = []
            for v in data.get('vulnerabilities', {}).get('list', []):
                adv = v.get('advisory', {})
                vulns.append({'package': v.get('package', {}).get('name'),
                              'version': v.get('package', {}).get('version'),
                              'vulnerability_id': adv.get('id'), 'severity': 'HIGH',
                              'source': 'cargo_audit'})
            return {'ecosystem': 'rust', 'vulnerabilities': vulns}
        except Exception as e:
            return {'ecosystem': 'rust', 'vulnerabilities': [], 'error': str(e)}

    def _update_summary(self, results):
        for v in results['vulnerabilities']:
            s = v.get('severity', '').upper()
            results['summary']['total'] += 1
            if s in results['summary']:
                results['summary'][s.lower()] += 1

    def generate_remediation_plan(self, vulnerabilities: List[Dict]) -> Dict:
        critical_high = [v for v in vulnerabilities if v.get('severity', '').upper() in ['CRITICAL', 'HIGH']]
        return {
            'immediate_actions': [{'package': v['package'], 'current': v.get('version'),
                                    'fixed_in': v.get('fixed_in', 'latest'), 'severity': v['severity']}
                                   for v in critical_high[:20]],
            'automation_scripts': {
                'npm':   'npm audit fix && npm update',
                'pip':   'pip-audit --fix && safety check',
                'go':    'go get -u ./... && go mod tidy',
                'cargo': 'cargo update && cargo audit'
            }
        }

    def generate_sbom(self, ecosystems: Dict) -> Dict:
        sbom = {'bomFormat': 'CycloneDX', 'specVersion': '1.4',
                'serialNumber': f'urn:uuid:{datetime.now().timestamp()}',
                'components': []}
        for eco, data in ecosystems.items():
            for v in data.get('vulnerabilities', []):
                sbom['components'].append({
                    'type': 'library', 'name': v.get('package'),
                    'version': v.get('version'),
                    'purl': f"pkg:{eco}/{v.get('package')}@{v.get('version')}"
                })
        return sbom
```

---

## 2. Vulnerability Prioritization

```python
class VulnerabilityPrioritizer:
    def calculate_priority_score(self, v: Dict) -> float:
        cvss = v.get('cvss_score', 0) or 0
        exploit = 1.0 if v.get('exploit_available') else 0.5
        fixable = 1.0 if v.get('fixed_in') else 0.3
        return round(cvss * 0.4 + exploit * 2.0 + fixable * 1.0, 2)

    def prioritize(self, vulnerabilities: List[Dict]) -> List[Dict]:
        for v in vulnerabilities:
            v['priority_score'] = self.calculate_priority_score(v)
        return sorted(vulnerabilities, key=lambda x: x['priority_score'], reverse=True)
```

---

## 3. Supply Chain Security

```python
def check_supply_chain_security(dependencies):
    issues = []
    for pkg, info in dependencies.items():
        # Typosquatting check (Levenshtein distance ≤ 2 from popular packages)
        common = ['react','express','lodash','axios','webpack','babel','jest','typescript']
        for legit in common:
            dist = levenshtein_distance(pkg.lower(), legit)
            if 0 < dist <= 2:
                issues.append({'type': 'typosquatting', 'package': pkg,
                                'severity': 'high', 'similar_to': legit})
        # Maintainer changes, suspicious patterns...
    return issues
```

---

## 4. License Compliance

```python
FORBIDDEN_LICENSES = {'GPL-2.0', 'GPL-3.0', 'AGPL-3.0', 'SSPL-1.0'}
ALLOWED_LICENSES = {'MIT', 'Apache-2.0', 'BSD-2-Clause', 'BSD-3-Clause', 'ISC', 'MPL-2.0'}

def check_license_compliance(dependencies):
    violations = []
    for pkg, info in dependencies.items():
        lic = info.get('license', 'UNKNOWN')
        if lic in FORBIDDEN_LICENSES:
            violations.append({'package': pkg, 'license': lic,
                                'severity': 'critical', 'action': 'Replace immediately'})
        elif lic not in ALLOWED_LICENSES:
            violations.append({'package': pkg, 'license': lic,
                                'severity': 'medium', 'action': 'Legal review required'})
    return violations
```

---

## 5. CI/CD Integration

```yaml
name: Dependency Security Scan
on:
  push:
    branches: [main]
  schedule:
    - cron: "0 2 * * *"   # daily

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: NPM Audit
        run: npm audit --json > npm-audit.json || true; npm audit --audit-level=moderate

      - name: Python Safety
        run: |
          pip install safety pip-audit
          safety check --json --output safety.json || true
          pip-audit --format=json --output=pip-audit.json || true

      - name: Go vulncheck
        run: |
          go install golang.org/x/vuln/cmd/govulncheck@latest
          govulncheck -json ./... > govulncheck.json || true

      - name: Fail on critical
        run: |
          CRITICAL=$(grep -o '"severity":"CRITICAL"' *.json 2>/dev/null | wc -l || echo 0)
          [ "$CRITICAL" -gt 0 ] && echo "❌ $CRITICAL critical vulnerabilities!" && exit 1

      - uses: actions/upload-artifact@v4
        with:
          name: dep-scan-results
          path: "*.json"
```

---

## 6. Automated Update Scripts

```bash
#!/bin/bash
set -euo pipefail
ECOSYSTEM="$1"; UPDATE_TYPE="${2:-patch}"

update_npm() {
    npm audit --audit-level=moderate || true
    [ "$UPDATE_TYPE" = "patch" ] && npm update --save
    [ "$UPDATE_TYPE" = "minor" ] && npx npm-check-updates -u --target minor && npm install
    npm test && npm audit --audit-level=moderate
}
update_python() { pip install --upgrade pip; pip-audit --fix; safety check; pytest; }
update_go()     { go get -u ./...; go mod tidy; govulncheck ./...; go test ./...; }
update_rust()   { cargo update; cargo audit; cargo test; }

case "$ECOSYSTEM" in
    npm) update_npm ;; python) update_python ;;
    go)  update_go  ;; rust)   update_rust   ;;
    *) echo "Unknown: $ECOSYSTEM"; exit 1 ;;
esac
```

---

## 7. Markdown Report Generator

```python
def generate_report(scan_results: Dict) -> str:
    s = scan_results['summary']
    report = f"""# Dependency Vulnerability Report
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- Total: {s['total']} | 🔴 Critical: {s['critical']} | 🟠 High: {s['high']} | 🟡 Medium: {s['medium']} | 🟢 Low: {s['low']}

## Critical & High Findings\n"""
    for v in [x for x in scan_results['vulnerabilities']
              if x.get('severity','').upper() in ['CRITICAL','HIGH']][:20]:
        report += f"\n### {v.get('package')} — {v.get('vulnerability_id','')}\n"
        report += f"- Severity: {v.get('severity')} | Version: {v.get('version')} | Fixed in: {v.get('fixed_in','N/A')}\n"
        if v.get('cve'): report += f"- CVEs: {', '.join(v['cve'])}\n"
    return report
```

---

## Tool Installation

```bash
# Python ecosystem
pip install safety pip-audit pipenv pip-licenses

# JavaScript
npm install -g snyk npm-check-updates

# Go
go install golang.org/x/vuln/cmd/govulncheck@latest

# Rust
cargo install cargo-audit
```

---

## Best Practices

1. Run scans daily via scheduled CI/CD — not just on push
2. Prioritize by CVSS score + exploit availability, not severity label alone
3. Auto-update patch versions; require manual review for minor/major
4. Always run full test suite after dependency updates
5. Maintain SBOM (CycloneDX or SPDX format) in source control
6. Check licenses before adding new dependencies
7. Keep a rollback branch before major update batches
8. Block merges on critical vulnerabilities (CI gate)
