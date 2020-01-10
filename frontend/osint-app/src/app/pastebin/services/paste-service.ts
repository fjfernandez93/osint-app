import {Injectable} from '@angular/core';
import {HttpClient, HttpParams} from '@angular/common/http';
import {Observable} from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class PastesService {

    constructor(private http: HttpClient) {}

    findPastes(
        filter_by = '', pageNumber = 0, pageSize = 3, orderBy = 'id', order = 'asc' // , filter = '', sortOrder = 'asc',
        ):  Observable<any> {

        return this.http.get('http://localhost:5000/paste', {
            params: new HttpParams()
                .set('filters', filter_by)
                .set('orderBy', orderBy)
                .set('order', order)
                .set('pageNumber', pageNumber.toString())
                .set('pageSize', pageSize.toString())
        });
    }

    getPasteContent(id_paste: number): Observable<any> {
        return this.http.get(`http://localhost:5000/paste/content/${id_paste}`);
    }
}
