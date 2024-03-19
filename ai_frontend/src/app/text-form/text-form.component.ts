import { Component } from '@angular/core';
import { LlmService } from '../llm.service';
import { OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';

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
  constructor(private llmService: LlmService){
  }



  ngOnInit(): void {
    console.log('nothin')
  }
// 
  postText(){
    this.llmService.postText(this.inputText.value).subscribe((response: PIIResponse[]) => {
      console.log(response)
    })
  }
}
