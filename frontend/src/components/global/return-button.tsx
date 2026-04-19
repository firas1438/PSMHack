"use client";

import { ArrowLeft } from "lucide-react";
import Link from "next/link";

import { Button } from "@/components/ui/button";
import { cn } from "@/lib";

type ReturnButtonProps = {
  href?: string;
  label?: string;
  className?: string;
};

export function ReturnButton({
  href = "/",
  label = "Return",
  className,
}: ReturnButtonProps) {
  return (
    <Button variant="ghost" size="lg" className={cn("gap-2", className)} asChild>
      <Link href={href}>
        <ArrowLeft className="size-4 shrink-0 text-primary" aria-hidden />
        {label}
      </Link>
    </Button>
  );
}
