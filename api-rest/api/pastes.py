from model.models import PasteData, PasteSchema, HitData
import connexion

paste_data = PasteData()
hit_data = HitData()


def search() -> dict:

    args = connexion.request.args
    if 'pageNumber' in args.keys() and 'pageSize' in args.keys():

        page_number = int(args['pageNumber'])
        page_size = int(args['pageSize'])
        order_by = args['orderBy'] if 'orderBy' in args.keys() else 'id'
        order = args['order'] if 'order' in args.keys() else 'asc'
        filters = args['filters'] if 'filters' in args.keys() else ''

        pastes, count = paste_data.get_page(page_number, page_size, order_by, order, filters)
    else:
        pastes = paste_data.get_all()
        count = len(pastes)

    paste_schema = PasteSchema(many=True)
    print(len(pastes))
    data = paste_schema.dump(pastes).data

    total = {'payload': data, 'length': count}
    return total


def content(id_paste) -> str:
    paste = paste_data.get_by_id(id_paste)
    result = dict()
    with open(paste.file_path, 'r') as f:
        result['content'] = f.read()

    result['previous_id'] = paste_data.get_previous_id(paste.id)
    result['next_id'] = paste_data.get_next_id(paste.id)
    result['hit_count'] = len(hit_data.get_by(source_type='pastebin', source_id=paste.id))

    return result