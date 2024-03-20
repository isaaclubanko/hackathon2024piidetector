import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';


interface PIIResponse {
  word: string,
  entityGroup: string
}

@Injectable({
  providedIn: 'root'
})
export class LlmService {

  constructor(
    private http: HttpClient
  ) { }

  public refreshAPI(){
    return this.http.get<string>('/api/')
  }

  public postText(inputText:string){
    return this.http.post<PIIResponse[]>('/api/detect_pii/', {text_input: inputText})
  }

}
