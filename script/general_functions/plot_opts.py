def process_res(results):
    sc = None
    obj_data = None
    var = None
    filenames = []
    unit = None
    for r in results:
        filenames.append(r[0])
        if sc is None and r[1] is not None:
            sc = r[1]
        if obj_data is None and r[2] is not None:
            obj_data = r[2]
        if var is None and r[3] is not None:
            var = r[3]
            unit = r[4]
    if var is not None:
        var = var[0]
    print(r)
    return filenames, sc, obj_data, var, unit
