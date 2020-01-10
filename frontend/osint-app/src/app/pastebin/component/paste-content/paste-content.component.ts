import { Component, OnInit } from '@angular/core';
import {PastesService} from '../../services/paste-service';
import {ActivatedRoute, Router} from '@angular/router';
import {ApiService} from '../../../shared/services/api';
import {PasteDataSource} from '../../paste.datasource';
import {SelectionModel} from '@angular/cdk/collections';

@Component({
  selector: 'app-paste-content',
  templateUrl: './paste-content.component.html',
  styleUrls: ['./paste-content.component.scss']
})
export class PasteContentComponent implements OnInit {

  content: string;
  idPaste: number;
  nextId: number;
  previousId: number;
  hitCount: number;
  hits: [];
  displayedColumns: string[] = ['select', 'entity', 'value'];
  showHitsTable = false;
  selection;

  constructor(private apiService: ApiService,
              private pasteService: PastesService,
              private activatedRoute: ActivatedRoute,
              private router: Router) {

      this.hitCount = 0;
      this.router.routeReuseStrategy.shouldReuseRoute = function() {
          return false;
      };

      const initialSelection = [];
      const allowMultiSelect = true;
      this.selection = new SelectionModel<any>(allowMultiSelect, initialSelection);
  }

  ngOnInit() {
      this.idPaste = +this.activatedRoute.snapshot.params['idPaste'];
      this.pasteService.getPasteContent(this.idPaste).subscribe(value => {
          this.content = value.content;
          this.nextId = value.next_id;
          this.previousId = value.previous_id;
          this.hitCount = value.hit_count;

          this.apiService.getSourceHits('pastebin', this.idPaste).subscribe(value2 => {
              this.hits = value2.payload;
              this.showHitsTable = true;
          });
      });
  }

  onClickPrevious() {
      this.router.navigate(['/pastebin/content', this.previousId]);
  }
  onClickNext() {
        this.router.navigate(['/pastebin/content', this.nextId]);
  }
  onClickHitsDetails() {
     this.apiService.getSourceHits('pastebin', this.idPaste).subscribe(value => {
         this.hits = value.payload;
         this.showHitsTable = true;
     });
  }

    /** Whether the number of selected elements matches the total number of rows. */
    isAllSelected() {
        const numSelected = this.selection.selected.length;
        const numRows = this.hits.length;
        return numSelected === numRows;
    }

    /** Selects all rows if they are not all selected; otherwise clear selection. */
    masterToggle() {
        this.isAllSelected() ?
            this.selection.clear() :
            this.hits.forEach(row => this.selection.select(row));
    }
}
