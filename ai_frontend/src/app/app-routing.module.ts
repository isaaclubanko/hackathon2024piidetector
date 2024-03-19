import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TextFormComponent } from './text-form/text-form.component';
const routes: Routes = [
  { path: '', component: TextFormComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
