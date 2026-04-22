"use client";

import { ArrowLeft } from "lucide-react";
import { useRouter } from 'next/navigation'
import { Button } from "@/components/ui/button";
import { cn } from "@/lib";

type ReturnButtonProps = {
  label?: string;
  className?: string;
};

export function ReturnButton({ label = "Return", className }: ReturnButtonProps) {
  const router = useRouter()

  return (
    <Button variant="ghost" onClick={() => router.back()} size="lg" className={cn("gap-2", className)}>
        <ArrowLeft className="size-4 shrink-0 text-primary" aria-hidden />
        {label}
    </Button>
  );
}
