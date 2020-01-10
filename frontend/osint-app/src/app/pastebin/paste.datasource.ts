import {PasteElement} from './pastebin.component';
import {BehaviorSubject, Observable, of} from 'rxjs';
import {catchError, filter, finalize} from 'rxjs/operators';
import {CollectionViewer, DataSource} from '@angular/cdk/collections';
import {PastesService} from './services/paste-service';

export class PasteDataSource implements DataSource<PasteElement> {

    private pastesSubject = new BehaviorSubject<PasteElement[]>([]);
    private loadingSubject = new BehaviorSubject<boolean>(false);
    private lengthSubject = new BehaviorSubject<number>(0);

    public loading$ = this.loadingSubject.asObservable();
    public pastesLength = this.lengthSubject.asObservable();

    public totalLength;
    constructor(private pastesService: PastesService) {}

    connect(collectionViewer: CollectionViewer): Observable<PasteElement[]> {
        return this.pastesSubject.asObservable();
    }

    disconnect(collectionViewer: CollectionViewer): void {
        this.pastesSubject.complete();
        this.loadingSubject.complete();
    }

    loadPastes(filter_by = '', pageIndex = 0, pageSize = 3, orderBy = 'id', order = 'asc') {

        this.loadingSubject.next(true);

        this.pastesService.findPastes(
            filter_by, pageIndex, pageSize, orderBy, order).pipe(
            catchError(() => of([])),
            finalize(() => this.loadingSubject.next(false))
        )
            .subscribe((pastes) => {
                console.log(pastes);
                this.totalLength = pastes['length'];
                this.lengthSubject.next(pastes['length']);
                this.pastesSubject.next(pastes['payload']);
            });
    }
}
