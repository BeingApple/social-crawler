package com.crawler.domain.entity;

import jakarta.persistence.*;
import lombok.Getter;

import java.time.LocalDateTime;

@Entity
@Table(name = "social_platform")
@Getter
public class SocialPlatform {

    @Id
    @Column(name = "platform_id", length = 50)
    private String platformId;

    @Column(nullable = false, length = 100)
    private String platformName;

    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;
}