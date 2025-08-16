import { Controller, Get } from '@nestjs/common';
import { ParserService } from './parser.service';

@Controller('parser')
export class ParserController {
  constructor(private readonly parserService: ParserService) {}

  @Get()
  async parse() {
    return await this.parserService.parseAllProductsFromMainPage();
  }
}
