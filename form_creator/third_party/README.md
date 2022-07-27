# Third Party
This application gives users the ability to use certain third-party packages to enhance their experience. As some of these third party packages are optional, this directory provides a safe way to import them. This is done by providing a wrapper which either imports the package or uses a fallback object.

To extend this, directory where the name is the same as the package name. The root of any new project should have a `pypi.txt` file which should contain the URL to the PyPI project page.

Create subdirectories accordingly to mimic the structure of the package. This would then mean that instead of:

```python
from adminsortable2.admin import SortableAdminMixin
```

We could instead have:

``` python
from third_party.adminsortable2.admin import SortableAdminMixin
```

When creating wrappers, only objects that are used within the code should be wrapped. This is avoid bloat in the codebase.
