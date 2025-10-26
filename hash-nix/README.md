# Hash Nix

Calculates a hash required for packaging software via Nix flakes


## Example

```nix
{ buildGoModule, fetchFromGitHub }:

buildGoModule {
  pname = "vmatch";
  version = "1.0.15";

  src = fetchFromGitHub {
    owner = "anttiharju";
    repo = "vmatch";
    rev = "8b56182b913d6c8a6a4936bcc98fd39276ecb30f";
    hash = "sha256-JxFnSYUt7/ZzsI6oAk8Jlwv3YmiMJLzhejNDqQQ/El4="; # nix-prefetch-github anttiharju vmatch --rev 8b56182b913d6c8a6a4936bcc98fd39276ecb30f | jq -r '.hash'
  };

  vendorHash = null;
}
```
