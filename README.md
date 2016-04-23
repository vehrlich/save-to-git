# save-to-git
Swift python/request/json/git coding event

######Configuration
Create file `configuration.py` and set your git name and your token there

```
configuration.py
git_name = "someuser"
git_token = "yyyzzxyyyzxxzxzzzzxzxxz"
```

######Run the script
./save_to_git.py <owner> <api_token> <local file path> <reponame>/<file path>

######Example
./save_to_git.py someuser yyyzzxyyyzxxzxzzzzxzxxz bp-1-0.xml best_product/bp-1-0/bp-1-0.xml
