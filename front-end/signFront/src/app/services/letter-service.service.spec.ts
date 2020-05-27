import { TestBed } from '@angular/core/testing';

import { LetterServiceService } from './letter-service.service';

describe('LetterServiceService', () => {
  let service: LetterServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(LetterServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
