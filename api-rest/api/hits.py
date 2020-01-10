from model.models import HitData, HitSchema


hit_data = HitData()


def get_by_source(source_type, source_id) -> dict():

    hits = hit_data.get_by(source_type=source_type, source_id=source_id)

    hit_schema = HitSchema(many=True)
    data = hit_schema.dump(hits).data

    result = {'payload': data, 'length': len(hits)}
    return result