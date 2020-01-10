import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PastebinComponent } from './pastebin.component';
import {TranslateModule} from '@ngx-translate/core';
import {PastebinRoutingModule} from './pastebin-routing.module';
import { MatSliderModule } from '@angular/material/slider';
import {MatButtonModule} from '@angular/material/button';
import {
    MatCheckboxModule, MatInputModule, MatPaginatorModule, MatProgressSpinnerModule,
    MatSortModule, MatTableModule
} from '@angular/material';
import {ApiService} from '../shared/services/api';
import {PastesService} from './services/paste-service';
import { PasteContentComponent } from './component/paste-content/paste-content.component';
import {StatModule} from '../shared/modules';

@NgModule({
    imports: [
        CommonModule,
        TranslateModule,
        PastebinRoutingModule,
        MatSliderModule,
        MatButtonModule,
        MatTableModule,
        MatInputModule,
        MatPaginatorModule,
        MatProgressSpinnerModule,
        MatSortModule,
        StatModule,
        MatCheckboxModule
    ],
        declarations: [PastebinComponent, PasteContentComponent],
    providers: [ApiService, PastesService]
})
export class PastebinModule { }
