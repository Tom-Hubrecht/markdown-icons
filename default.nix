{
  sources ? import ./npins,
  pkgs ? import sources.nixpkgs { },
}:

let
  deploy-pypi = pkgs.writeShellApplication {
    name = "deploy-pypi";

    runtimeInputs = [
      (pkgs.python3.withPackages (ps: [
        ps.setuptools
        ps.build
        ps.twine
      ]))
    ];

    text = ''
      # Clean the repository
      rm -r dist markdown_icons.egg-info

      python -m build
      twine upload dist/*
    '';
  };
in

{
  devShell = pkgs.mkShell {
    name = "markdown-icons";

    packages = [ (pkgs.python3.withPackages (ps: [ ps.markdown ])) ];
  };

  publishShell = pkgs.mkShell {
    name = "markdown-icons.publish";

    packages = [ deploy-pypi ];
  };
}
