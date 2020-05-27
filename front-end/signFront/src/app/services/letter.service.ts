import { Injectable } from '@angular/core';
import {baseURL} from '../shared/base'
@Injectable({
  providedIn: 'root'
})
export class LetterService {
  constructor() { }

  getLetterToRecognize() {
    return 'A'
  }
}
