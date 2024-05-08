{
  sources ? import ./npins,
  pkgs ? import sources.nixpkgs { },
}:

{
  devShell = pkgs.mkShell {
    name = "markdown-icons";

    packages = [ (pkgs.python3.withPackages (ps: [ ps.markdown ])) ];
  };

  publishShell = pkgs.mkShell {
    name = "markdown-icons.publish";

    packages = [
      (pkgs.python3.withPackages (ps: [
        ps.setuptools
        ps.build
        ps.twine

        ps.markdown
      ]))
    ];
  };
}
