package com.musinsa.crawler.domain.entity;

import jakarta.persistence.*;
import lombok.Getter;

import java.time.LocalDateTime;

@Entity
@Table(name = "brand_assignee")
@Getter
public class BrandAssignee {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long assigneeId;

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "brand_id", nullable = false)
    private Brand brand;

    @Column(nullable = false, length = 50)
    private String platformId;

    @Column(nullable = false, length = 50)
    private String assigneeName;

    @Column(nullable = false, length = 100)
    private String accountId;

    @Column(nullable = false, length = 30)
    private String accountType;

    @Column(name = "is_active", nullable = false)
    private boolean active;

    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @Column(nullable = false)
    private LocalDateTime updatedAt;
}
