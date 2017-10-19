def processRef(ref):
    surah = int(ref.split(':')[0])
    min_ayah = int(ref.split(':')[1].split('-')[0])

    try:
        max_ayah = int(ref.split(':')[1].split('-')[1]) + 1
    except IndexError:
        max_ayah = min_ayah + 1

    return [surah, min_ayah, max_ayah]