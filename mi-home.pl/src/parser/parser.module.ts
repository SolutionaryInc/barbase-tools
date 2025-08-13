import { Module } from '@nestjs/common';
import { ParserService } from './parser.service';
import { ParserController } from './parser.controller';
import { PrismaService } from 'src/prisma/prisma.service';

@Module({
  controllers: [ParserController],
  providers: [ParserService, PrismaService],
})
export class ParserModule {}
