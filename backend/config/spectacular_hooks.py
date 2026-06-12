def exclude_non_api_paths(endpoints, **kwargs):
    excluded_prefixes = [
        "/admin/",
        "/api/token/",
        "/api/auth/",
    ]

    return [
        (path, path_regex, method, callback)
        for path, path_regex, method, callback in endpoints
        if not any(path.startswith(prefix) for prefix in excluded_prefixes)
    ]
