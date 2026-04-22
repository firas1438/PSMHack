"use client";

import Image from "next/image"; // Import Image component
import Link from "next/link";

import Container from "@/components/global/container";
import { ReturnButton } from "@/components/global/return-button";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

const features = [
  {
    title: "Water Livability",
    description: "Assess seawater quality from sample metrics and predict livability class",
    image: "/water.png",
    href: "/livability",
    ctaText: "Test Livability",
  },
  {
    title: "Algae Detection",
    description: "Detect and segment algae blooms in coastal satellite imagery",
    image: "/algaes.png", 
    href: "/algae",
    ctaText: "Detect Algae",
  },
];

export function FeatureSelect() {
  return (
    <div className="relative mx-auto w-full max-w-7xl px-4 pt-6 md:pt-10">
      <div className="relative mb-10 space-y-0 sm:mb-8">
        <Container className="w-full">
          <div className="flex items-start justify-between gap-3 sm:items-center sm:gap-4">
            <h1 className="min-w-0 max-w-2xl font-heading text-3xl font-semibold tracking-tight md:text-4xl">
              Choose a Feature
            </h1>
            <ReturnButton className="shrink-0" />
          </div>
        </Container>
        <Container delay={0.1} className="w-full">
          <p className="mt-3 max-w-2xl text-pretty text-muted-foreground sm:mt-4">
            Select how you'd like to analyze coastal water data. Pick between assessing seawater livability or detecting algae blooms.
          </p>
        </Container>
      </div>

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
                    <div className="relative size-56 transition-transform duration-300 group-hover:scale-110">
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
    </div>
  );
}