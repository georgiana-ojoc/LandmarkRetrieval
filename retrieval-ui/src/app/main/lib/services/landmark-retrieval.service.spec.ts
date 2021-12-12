/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { LandmarkRetrievalService } from './landmark-retrieval.service';

describe('Service: LandmarkRetrieval', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [LandmarkRetrievalService]
    });
  });

  it('should ...', inject([LandmarkRetrievalService], (service: LandmarkRetrievalService) => {
    expect(service).toBeTruthy();
  }));
});
