import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {PastebinComponent} from './pastebin.component';
import {PasteContentComponent} from './component/paste-content/paste-content.component';

const routes: Routes = [
    {
        path: '', component: PastebinComponent
    },
    {
        path: 'content/:idPaste', component: PasteContentComponent
    },
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class PastebinRoutingModule {}
