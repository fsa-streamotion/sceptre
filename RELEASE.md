# How to release

This documents how to release the Fox fork of Sceptre.

## Merge upstream

To raise a PR to merge upstream master into develop:

- Go to https://github.com/fsa-streamotion/sceptre/compare/develop...Sceptre:master
- PR title Merge upstream master => develop

## Bump version

Run the `bump_verion.sh` script, e.g.

```text
bash bump_verion.sh 2.10.0
```

## make dist

Run `make dist`. A `whl` file and a `.tar.gz` file is created inside `./dist`.

## Create GitHub release

- Go to https://github.com/fsa-streamotion/sceptre

- On the right-hand side, click [Releases](https://github.com/fsa-streamotion/sceptre/releases).

- Click *Draft a new release*

    * In *Choose a tag* write a new tag like `v2.10.0`.
    * In *Release title* also write the tag like `v2.10.0`.
    * Drag and drop the `whl` and `.tar.gz` to the screen where indicated.
    * Click *Publish release*.

That's it. The new release should now be available to install.

## See also

The upstream release workflow is documented in the the `Release Workflow` section [here](https://github.com/fsa-streamotion/sceptre/blob/02f6021589cd486868cf52bf9818e3afbd265fe6/.circleci/README.md#release-workflow).
