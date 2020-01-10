import {Component, OnInit, AfterViewInit, ViewChild, ElementRef} from '@angular/core';
import {ApiService} from '../shared/services/api';
import {MatPaginator, MatSort, MatTable} from '@angular/material';
import {PasteDataSource} from './paste.datasource';
import {PastesService} from './services/paste-service';
import {debounceTime, distinctUntilChanged, tap} from 'rxjs/operators';
import {fromEvent, merge} from 'rxjs';


export interface PasteElement {
    id: number;
    key: string;
    full_url: string;
    file_path: string;
}

@Component({
    selector: 'app-pastebin',
    templateUrl: './pastebin.component.html',
    styleUrls: ['./pastebin.component.scss']
})
export class PastebinComponent implements OnInit, AfterViewInit {

    displayedColumns: string[] = ['id', 'key', 'full_url', 'file_path', 'actions'];
    dataSource: PasteDataSource;
    @ViewChild(MatTable, {static: false}) table: MatTable<any>;
    @ViewChild(MatPaginator, {static: false}) paginator: MatPaginator;
    @ViewChild(MatSort, {static: false}) sort: MatSort;
    @ViewChild('inputSearch', {static: false}) inputSearch: ElementRef;

    constructor(private apiService: ApiService, private pastesService: PastesService) {
    }

    ngOnInit() {
        // this.apiService.getAllPastes().subscribe(value => {
        //     // console.log(value);
        //     this.dataSource2 = value;
        //     this.table.renderRows();
        //
        // });
        this.dataSource = new PasteDataSource(this.pastesService);
        this.dataSource.loadPastes('', 1,  10);
    }

    ngAfterViewInit() {

        fromEvent(this.inputSearch.nativeElement, 'keyup')
            .pipe(
                debounceTime(150),
                distinctUntilChanged(),
                tap(() => {
                    this.paginator.pageIndex = 0;
                    this.loadPastesPage();
                })
            )
            .subscribe();

        this.sort.sortChange.subscribe(() => this.paginator.pageIndex = 0);

        merge(this.paginator.page, this.sort.sortChange)
            .pipe(
                tap(() => this.loadPastesPage())
            )
            .subscribe();
    }

    loadPastesPage() {
        this.dataSource.loadPastes(
            this.inputSearch.nativeElement.value,
            this.paginator.pageIndex,
            this.paginator.pageSize,
            this.sort.active,
            this.sort.direction);
    }

    showPasteContent(paste_id: number) {
        alert(paste_id);
    }
}
