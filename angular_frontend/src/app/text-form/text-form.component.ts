import { Component } from '@angular/core';
import { LlmService } from '../llm.service';
import { OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { BehaviorSubject, Observable, catchError, tap } from 'rxjs';
import { PIIResponseModel } from '../models/pii-response.model'

// interface PIIResponse {
//   word: string,
//   entity_group: string
// }

@Component({
  selector: 'app-text-form',
  templateUrl: './text-form.component.html',
  styleUrls: ['./text-form.component.css']
})
export class TextFormComponent implements OnInit{

  public inputText = new FormControl('', [Validators.required]);
  public showTextBox = false;
  public piiDetections$: Observable<PIIResponseModel[]> = new Observable()
  public modelLoaded = new BehaviorSubject<boolean>(false);

  constructor(private llmService: LlmService){
  }



  ngOnInit(): void {
    this.llmService.refreshAPI().pipe(
      catchError((x:any)=>{
        console.log("Error in refreshAPI")
        throw x 
      }),
      tap( 
        (response: string) => {
          this.modelLoaded.next(true);
        }
      )
    ).subscribe()
    this.modelLoaded.subscribe((loaded: boolean) => {
      if (loaded){
        this.showTextBox = true;
      }
    })
  }

  postText(){
    if (this.inputText.value !== null) {
      this.piiDetections$ = this.llmService.postText(this.inputText.value)
    }
  }
}
