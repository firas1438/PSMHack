"use client";

import Image from "next/image";
import Link from "next/link";

import Container from "@/components/global/container";
import { ReturnButton } from "@/components/global/return-button";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle, } from "@/components/ui/card";
import { Header } from "@/components/global/header";
import Wrapper from "@/components/global/wrapper";

const features = [
  {
    title: "Water Livability",
    description: "Assess seawater quality from sample metrics and predict livability class",
    image: "/water.png",
    href: "/features/livability",
    ctaText: "Test Livability",
  },
  {
    title: "Algae Detection",
    description: "Detect and segment algae blooms in coastal satellite imagery",
    image: "/algaes.png",
    href: "/features/algae",
    ctaText: "Detect Algae",
  },
];

export default function SelectPage() {
  return (
    <div className="flex min-h-screen flex-col px-3 lg:px-0">
      <main className="flex-1 py-20">
        <Wrapper className="relative pt-6 md:pt-10">

          {/* header */}
          <Header
            title="Choose a Feature"
            description="Select how you'd like to analyze coastal water data. Pick between assessing seawater livability or detecting algae blooms."
          />

          {/* features */}
          <Container delay={0.2} className="w-full">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {features.map((feature) => {
                return (
                  <Link key={feature.href} href={feature.href} className="block h-full group">
                    <Card className="h-full border-border/80 shadow-md shadow-black/10 ring-1 ring-border/40 hover:border-primary/50 hover:shadow-lg transition-all duration-300 cursor-pointer flex flex-col overflow-hidden">
                      <CardHeader>
                        <CardTitle>{feature.title}</CardTitle>
                      </CardHeader>

                      <CardContent className="flex-1 flex items-center justify-center">
                        <div className="relative size-60 transition-transform duration-300 group-hover:scale-110">
                          <Image src={feature.image} alt={feature.title} fill className="object-contain" />
                        </div>
                      </CardContent>

                      <div className="px-6 pt-4 pb-2 border-t border-border/60 bg-muted/20">
                        <CardDescription className="mb-5 text-sm">
                          {feature.description}
                        </CardDescription>
                        <Button className="w-full">{feature.ctaText}</Button>
                      </div>
                    </Card>
                  </Link>
                );
              })}
            </div>
          </Container>

        </Wrapper>
      </main>
    </div>
  );
}
