import React from "react";
import Image from "next/image";
import Wrapper from "@/components/global/wrapper";
import Container from "@/components/global/container";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";

const FAQS = [
  {
    question: "What problem does our platform solve?",
    answer: "Aqualog helps coastal teams track pollution pressure by turning seawater samples and satellite views into clear livability scores and algae warnings.",
  },
  {
    question: "How does seawater livability analysis work?",
    answer: "Our first model reads your sample parameters (salinity, nutrients, temperature, and related indicators) and estimates whether conditions are favorable for healthy marine life in that area.",
  },
  {
    question: "Does the algae model need drones or ships?",
    answer: "No. You upload a satellite image covering the region; the second model classifies whether algae growth signatures appear in that scene, without extra hardware beyond your usual data sources.",
  },
  {
    question: "Who is it designed for?",
    answer: "It is designed for researchers, biologists and environmental agencies who monitor coastal waters and need faster, comparable insight across sites and time.",
  },
  {
    question: "What makes our solution different?",
    answer: "Instead of generic dashboards, Aqualog combines two focused AI tools: seawater livability scoring and satellite algae classification for taking early action against maritime hazards.",
  }
];

const Faq = () => {
  return (
    <section id="faq" className="flex flex-col items-center justify-center relative w-full py-16 lg:py-24 overflow-hidden px-4 sm:px-0">
      <div className="absolute top-0 -right-1/3 -z-10 ml-auto w-4/5 h-32 lg:h-48 rounded-full blur-[5rem] bg-[radial-gradient(86.02%_172.05%_at_50%_-40%,rgba(18,139,135,0.7)_0%,rgba(5,5,5,0)_80%)]"></div>

      <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,0.1)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.1)_1px,transparent_1px)] bg-size-[3rem_3rem] mask-[radial-gradient(ellipse_60%_70%_at_90%_0%,#000_20%,transparent_70%)] h-full -z-10" />

      <Wrapper>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-16 lg:gap-6">
          <Container>
            <div className="flex flex-col">
              <div className="flex flex-col items-start justify-start lg:items-center lg:justify-center lg:items-start lg:justify-start">
                <h2 className="text-3xl lg:text-4xl font-semibold text-left lg:text-start tracking-tight">
                  Frequently asked questions
                </h2>
                <p className="text-base lg:text-lg font-normal text-muted-foreground text-left lg:text-start mt-2 max-w-md">
                  Here you will find the answers to the most commonly asked questions & answers.
                </p>
              </div>
              <div className="mt-10">
                <Accordion type="single" collapsible className="w-full">
                  {FAQS.map((faq, index) => (
                    <AccordionItem key={index} value={`item-${index}`}>
                      <AccordionTrigger className="text-base font-base font-semibold">
                        {faq.question}
                      </AccordionTrigger>
                      <AccordionContent className="text-base text-muted-foreground">
                        {faq.answer}
                      </AccordionContent>
                    </AccordionItem>
                  ))}
                </Accordion>
              </div>
            </div>
          </Container>

          <Container>
            <div className="col-span-1 w-full z-10 flex items-center justify-center lg:justify-end">
              <div className="relative w-full max-w-md">
                <Image src="/faq.png" alt="FAQ" width={1024} height={1024} className="w-full h-auto object-contain" />
              </div>
            </div>
          </Container>
        </div>
      </Wrapper>
    </section>
  );
};

export default Faq
