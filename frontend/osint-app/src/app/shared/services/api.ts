import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class ApiService {

    constructor(private httpClient: HttpClient) {}

    getAllPastes(): Observable<any> {
        return this.httpClient.get('http://localhost:5000/paste');
    }

    // Hits
    getSourceHits(source_type: string, source_id: number): Observable<any> {
        return this.httpClient.get(`http://localhost:5000/hit/${source_type}/${source_id}`);
    }

}
