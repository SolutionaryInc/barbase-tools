import { Injectable, Logger } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import * as puppeteer from 'puppeteer';
import { PrismaService } from 'src/prisma/prisma.service';

export interface Product {
  title: string;
  barcode: string;
  image: string;
  url: string;
}

@Injectable()
export class ParserService {
  constructor(
    private readonly prismaService: PrismaService,
    private readonly configService: ConfigService,
  ) {}

  private readonly logger = new Logger(ParserService.name);

  async parseAllProductsFromMainPage() {
    const mainUrl = this.configService.getOrThrow<string>('URL');

    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();
    await page.setUserAgent(
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115 Safari/537.36',
    );

    try {
      await page.goto(mainUrl, {
        waitUntil: 'domcontentloaded',
        timeout: 60000,
      });
      await page.waitForSelector('a.full-unstyled-link', { timeout: 60000 });

      const productLinks: string[] = await page.$$eval(
        'a.full-unstyled-link',
        (links) => links.map((el) => (el as HTMLAnchorElement).href),
      );

      for (const url of productLinks) {
        try {
          await page.goto(url, {
            waitUntil: 'domcontentloaded',
            timeout: 60000,
          });
          await page.waitForSelector('#pwzrswiper-img-0', { timeout: 60000 });

          const title = await page.$eval(
            'h1',
            (el) => el.textContent?.trim() || '',
          );
          const barcode = await page.$eval(
            '.barcode-wrapper',
            (el) => el.textContent?.replace('EAN:', '').trim() || '',
          );
          const image = await page.$eval(
            '#pwzrswiper-img-0',
            (el) => el.getAttribute('src') || '',
          );

          await this.prismaService.parser.upsert({
            where: {
              barcode,
            },
            update: {
              title,
              images: image,
            },
            create: {
              barcode,
              title,
              images: image,
            },
          });
          this.logger.log(`Parsed: ${title}`);
        } catch (error) {
          this.logger.error(error);
        }
      }

      await browser.close();
    } catch (error) {
      this.logger.error(error);
      await browser.close();
    }
  }
}
