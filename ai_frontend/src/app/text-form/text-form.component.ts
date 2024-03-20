import { Component } from '@angular/core';
import { LlmService } from '../llm.service';
import { OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { BehaviorSubject, of, catchError, tap } from 'rxjs';

interface PIIResponse {
  word: string,
  entityGroup: string
}

@Component({
  selector: 'app-text-form',
  templateUrl: './text-form.component.html',
  styleUrls: ['./text-form.component.css']
})
export class TextFormComponent implements OnInit{

  public inputText = new FormControl('', {nonNullable: true});
  public showTextBox = false;
  public piiDetections: any[] = []
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
    this.llmService.postText(this.inputText.value).subscribe((response: PIIResponse[]) => {
      this.piiDetections = response;
    })
  }
}
